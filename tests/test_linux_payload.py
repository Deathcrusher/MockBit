import sys
from pathlib import Path

from mockbit import linux_payload


def test_main_runs_simulation(monkeypatch, tmp_path):
    called = {}

    def fake_run_simulation(path: Path) -> None:
        called["path"] = path

    monkeypatch.setattr(linux_payload, "run_simulation", fake_run_simulation)
    monkeypatch.setattr(sys, "argv", ["linux_payload", "--path", str(tmp_path)])
    linux_payload.main()
    assert called["path"] == tmp_path

