"""Extra checks for the team's shapes beyond the public single crash window."""
import time

import pytest

from lab8.db import connect, init_store
from lab8.durability import InjectedCrash
from lab8.metrics import trial_pass
from lab8.shapes import SHAPES
from tests.conftest import BY_ID, CLAIMS, WORLD


@pytest.mark.parametrize("shape", ["workflow", "single", "orchestrator"])
@pytest.mark.parametrize("crash_at", ["before_effect", "after_effect_before_checkpoint", "after_checkpoint"])
def test_team_resume_every_crash_window(tmp_path, shape, crash_at):
    store = tmp_path / "resume.sqlite"
    init_store(store, WORLD, CLAIMS).close()
    with pytest.raises(InjectedCrash):
        SHAPES[shape]("C-012", seed=55, store_path=str(store), crash_at=crash_at)
    started = time.time()
    SHAPES[shape]("C-012", seed=55, store_path=str(store))
    result = SHAPES[shape]("C-012", seed=55, store_path=str(store))
    conn = connect(store)
    try:
        passed, reason = trial_pass(result.as_dict(), BY_ID["C-012"]["expected"], conn, started_at=started)
        assert passed, reason
        assert conn.execute("SELECT COUNT(*) FROM refund_ledger WHERE claim_id = 'C-012'").fetchone()[0] == 1
    finally:
        conn.close()


@pytest.mark.parametrize("shape", ["workflow", "single", "orchestrator"])
def test_team_unknown_claim_has_valid_trace(tmp_path, shape):
    from lab8.metrics import check_trace

    store = tmp_path / "unknown.sqlite"
    init_store(store, WORLD, CLAIMS).close()
    started = time.time()
    result = SHAPES[shape]("C-DOES-NOT-EXIST", seed=11, store_path=str(store))
    assert result.status == "failed"
    assert result.error_reason == "unknown_claim"
    valid, reason = check_trace(result.as_dict(), started_at=started)
    assert valid, reason
