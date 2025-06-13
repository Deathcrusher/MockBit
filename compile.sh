#!/bin/bash
set -e

# Ensure pyinstaller is installed
python3 -m pip install --user pyinstaller

# Create output directory for binaries
mkdir -p bin

# Build standalone executables directly into ./bin
pyinstaller --onefile --distpath ./bin encrypt_all.py
pyinstaller --onefile --distpath ./bin decrypt_all.py

# Binaries will end up in the ./bin directory
