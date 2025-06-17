import os
import sys
from pathlib import Path

sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
from mockbit.ransom_sim import run_simulation, restore_simulation, _xor_bytes


def test_ransom_sim(tmp_path):
    original = {}
    for i in range(20):
        f = tmp_path / f"file{i}.bin"
        data = os.urandom(64)
        f.write_bytes(data)
        original[f] = data

    run_simulation(tmp_path)

    note = tmp_path / "README_MOCKBIT_RESTORE.txt"
    assert note.exists()

    for f, data in original.items():
        assert not f.exists()
        locked = f.with_suffix(f.suffix + ".mocklock")
        assert locked.exists()
        enc = locked.read_bytes()
        assert _xor_bytes(enc) == data

def test_restore_sim(tmp_path):
    original = {}
    for i in range(5):
        f = tmp_path / f"orig{i}.txt"
        data = os.urandom(32)
        f.write_bytes(data)
        original[f] = data
    run_simulation(tmp_path)
    restore_simulation(tmp_path)
    for f, data in original.items():
        assert f.exists()
        assert f.read_bytes() == data
    assert not (tmp_path / "README_MOCKBIT_RESTORE.txt").exists()

