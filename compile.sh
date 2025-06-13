#!/bin/bash
set -e

# Ensure pyinstaller and required packages are installed
python3 -m pip install --user pyinstaller
python3 -m pip install --user -r requirements.txt

# Create output directory for binaries
mkdir -p bin

# Build standalone executables directly into ./bin
COMMON_OPTS="--onefile --distpath ./bin --hidden-import=Crypto --hidden-import=Crypto.Random --hidden-import=Crypto.Cipher --hidden-import=argon2"
pyinstaller $COMMON_OPTS encrypt_all.py
pyinstaller $COMMON_OPTS decrypt_all.py

# Binaries will end up in the ./bin directory
