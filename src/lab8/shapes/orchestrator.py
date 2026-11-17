"""Shape C — orchestrator plus read-only investigators. Student work.

1. Build a handoff with `lab8.handoff.make_handoff`. Allowed tools are read-only.
   Never put parent_secret, raw headers, or the full claim row into facts.
2. `lab8.runtime.run_readonly_investigators` runs those tools.
3. The orchestrator quotes from the investigator's order view and calls
   `durability.issue_refund`. Investigators have no write registry.
   Pass the full quote; the host subtracts earlier refunds on the same order.
   `lookup_refund_history` is a read-only tool you may hand to an investigator.
4. Trace the sanitized handoff, not the parent context.

An LLM summary of the parent context is not a sanitizer. Use the allowlist.

Trace contract v1 (docs/contracts.md): return a trace_path to a JSON file written in this run,
{"run_id": <same run_id>, "events": [...]}, on every return path including early
ones. `lab8.trace.Trace` does this; your own tracer is fine if it matches.
"""

from __future__ import annotations

from lab8.db import connect
from lab8.durability import issue_refund
from lab8.handoff import make_handoff
from lab8.mock_llm import complete
from lab8.runtime import dispatch, run_readonly_investigators
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
    # TODO CP2 (student): thay stub này bằng shape orchestrator theo các bước ở docstring đầu file.
    # TODO CP3 (student): truyền crash_at vào durability.issue_refund, không bắt InjectedCrash.
    conn = connect(store_path)
    try:
        budget = Budget()
        trace = Trace(make_run_id("orchestrator", claim_id, seed))
        proposal = 0
        status = "failed"
        reason = "unknown_claim"
        claim = dispatch(conn, budget, "get_claim_view", {"claim_id": claim_id}, worker=False)

        if claim["found"]:
            if not claim.get("order_id"):
                status, reason = "needs_info", "missing_order_id"
            else:
                complete(budget, seed=seed, purpose="plan", prompt="investigate_claim")
                handoff = make_handoff(
                    request_id=f"REQ-{claim_id}",
                    claim_id=claim_id,
                    task="check_applicable_policy",
                    facts={},
                    allowed_tools=["lookup_order", "lookup_policy", "compute_compensation"],
                )
                trace.add("handoff", handoff)
                investigated = run_readonly_investigators(
                    conn, budget, handoff, principal_id=claim["principal_id"]
                )
                order_view = investigated["tools"]["lookup_order"]
                trace.add("investigator", {"lookup_order": order_view})
                if not order_view["visible"]:
                    status, reason = "escalated", order_view["reason"]
                else:
                    quote = investigated["tools"]["compute_compensation"]
                    trace.add("quote", quote)
                    proposal = int(quote["amount_vnd"])
                    status, reason = "denied", quote["reason"]
                    complete(budget, seed=seed, purpose="draft", prompt=f"proposal={proposal}")
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
            shape="orchestrator",
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
