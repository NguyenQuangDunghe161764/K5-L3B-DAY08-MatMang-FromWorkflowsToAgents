"""Shape B — one ReAct agent. Student work.

Use `lab8.runtime.run_react` with max_steps=8. `decide` may pick a read tool.
It must not call `issue_refund`. After the loop, the host validates the quote
and is the only writer.

A decide() that trusts ticket text over the order row will fail hidden claims
where the customer overstates the delay or cites a superseded clause.

Per-order cap: an order may already have been refunded by an earlier claim.
The read tool `lookup_refund_history` shows how much. The host still enforces
the cap, so pass the full quote to `durability.issue_refund`, not a net amount.

Caps: stop at 8 steps. Count model calls in the Budget so cost stays comparable.

Trace contract v1 (docs/contracts.md): return a trace_path to a JSON file written in this run,
{"run_id": <same run_id>, "events": [...]}, on every return path including early
ones. `lab8.trace.Trace` does this; your own tracer is fine if it matches.
"""

from __future__ import annotations

from lab8.db import connect
from lab8.durability import issue_refund
from lab8.mock_llm import complete
from lab8.runtime import dispatch, run_react
from lab8.schemas import Budget, RunResult, make_run_id
from lab8.shapes.common import finish
from lab8.trace import Trace


def run_claim(
    claim_id: str,
    *,
    seed: int,
    store_path: str,
    crash_at: str | None = None,
) -> RunResult:
    # TODO CP2 (student): thay stub này bằng shape single theo các bước ở docstring đầu file.
    # TODO CP3 (student): truyền crash_at vào durability.issue_refund, không bắt InjectedCrash.
    conn = connect(store_path)
    try:
        budget = Budget()
        trace = Trace(make_run_id("single", claim_id, seed))
        claim = dispatch(conn, budget, "get_claim_view", {"claim_id": claim_id}, worker=False)

        def decide(observation):
            last_tool = observation.get("last_tool")
            complete(budget, seed=seed, purpose="react", prompt=f"next read after {last_tool}")
            if not claim["found"]:
                return {"final": {"status": "failed", "error_reason": "unknown_claim"}}
            if not claim.get("order_id"):
                return {"final": {"status": "needs_info", "error_reason": "missing_order_id"}}
            if last_tool is None:
                trace.add("agent_tool", {"tool": "lookup_order"})
                return {
                    "tool": "lookup_order",
                    "args": {"order_id": claim["order_id"], "principal_id": claim["principal_id"]},
                }
            result = observation["last_result"]
            if last_tool == "lookup_order":
                trace.add("lookup_order", result)
                if not result["visible"]:
                    return {"final": {"status": "escalated", "error_reason": result["reason"]}}
                trace.add("agent_tool", {"tool": "compute_compensation"})
                return {"tool": "compute_compensation", "args": {"order": result["order"]}}
            return {"final": {"quote": result}}

        investigation = run_react(
            conn, budget, observation={"claim": claim}, decide=decide, max_steps=8, worker=True
        )
        final = investigation["final"]
        quote = final.get("quote")
        proposal = 0
        status = final.get("status", "denied")
        reason = final.get("error_reason")
        if quote is not None:
            trace.add("quote", quote)
            proposal = int(quote["amount_vnd"])
            reason = quote["reason"]
            if proposal > 0:
                outcome = issue_refund(conn, claim_id, proposal, crash_at=crash_at)
                trace.add("refund", outcome)
                if outcome["ok"]:
                    status, reason = "resolved", None
                else:
                    status = "failed" if outcome["conflict"] else "denied"
                    reason = outcome["reason"]

        trace.add("decision", {"status": status, "reason": reason})
        return finish(
            conn,
            shape="single",
            claim_id=claim_id,
            seed=seed,
            status=status,
            proposal_amount=proposal,
            budget=budget,
            trace=trace,
            error_reason=reason,
        )
    finally:
        conn.close()
