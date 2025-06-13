#!/bin/bash
set -e

# Ensure a writable temporary directory on systems where /tmp is noexec
mkdir -p "$HOME/tmp"
export TMPDIR="$HOME/tmp"

# Ensure pip-installed executables are found
export PATH="$HOME/.local/bin:$PATH"

# Install build dependencies and invoke the Makefile
python3 -m pip install --user -r requirements.txt
python3 -m pip install --user pyinstaller

# Delegate the actual build to the Makefile
make "$@"
