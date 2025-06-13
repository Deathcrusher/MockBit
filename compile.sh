#!/bin/bash
set -e

# Install build dependencies and invoke the Makefile
python3 -m pip install --user -r requirements.txt
python3 -m pip install --user pyinstaller

# Delegate the actual build to the Makefile
make "$@"
