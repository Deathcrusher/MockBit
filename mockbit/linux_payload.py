from __future__ import annotations

"""Linux payload to run the ransomware simulation for EDR testing."""

import argparse
from pathlib import Path

from .ransom_sim import run_simulation


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Run the MockBit ransomware simulation on a target directory."
    )
    parser.add_argument(
        "--path", default=".", help="Directory to use (default: current directory)"
    )
    args = parser.parse_args()
    target = Path(args.path)
    run_simulation(target)
    print(f"Ransomware simulation executed on {target}")


if __name__ == "__main__":
    main()

