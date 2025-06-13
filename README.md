# Simple AES File Encrypt/Decrypt Scripts
# Einfache AES-Datei Verschl\xC3\xBCsselungs-/Entschl\xC3\xBCsselungsskripte

**Encrypt and decrypt all files in a folder (including subfolders) with AES-256-GCM.**
**Verschl\xC3\xBCssle und entschl\xC3\xBCssle alle Dateien in einem Ordner (inkl. Unterordner) mit AES-256-GCM.**

## Requirements
## Voraussetzungen

- Python 3.x
- Install [PyCryptodome](https://www.pycryptodome.org/) and [argon2-cffi](https://pypi.org/project/argon2-cffi/):
  ```
  pip3 install -r requirements.txt
  ```

### Compiled Version
### Kompilierte Version

- `make` builds standalone binaries in the `bin/` directory.
- The script `compile.sh` installs dependencies and then calls `make`.
- So run either
  ```
  make
  ```
  or
  ```
  ./compile.sh
  ```
- Afterwards you will find the executables in `bin/`. Use `make clean` to remove the build files.

## Usage
## Verwendung

### 1. Encrypt
### 1. Verschl\xC3\xBCsseln

- Adjust `START_PATH` in `encrypt_all.py` to your target directory.
- Run the script and enter a passphrase:
  ```
  python3 encrypt_all.py
  ```
- The passphrase is derived into a key using Argon2id.
- Parameters such as salt and time/memory cost are stored in `MOCKBIT_KEY.txt`.
- All files are encrypted as `.mock`; the originals are securely deleted.
- The generated BASE64 key will be printed – **be sure to keep it!**

### 2. Decrypt
### 2. Entschl\xC3\xBCsseln

- Adjust `START_PATH` in `decrypt_all.py` to the directory with the `.mock` files.
- Make sure `MOCKBIT_KEY.txt` is present and enter the same passphrase.
- Run the script:
  ```
  python3 decrypt_all.py
  ```
- The files will be restored and the `.mock` files removed.

## Notes
## Hinweise

- **Always test in a safe environment first!**
- Without the key nobody can recover the data.
- The script does not overwrite existing files when decrypting; it restores their original name.
- Further development is needed for backups or production use!

## Disclaimer
## Haftungsausschluss

Use at your own risk. No liability for data loss or misuse.
Benutzung auf eigene Gefahr. F\xC3\xBCr Datenverlust oder Missbrauch wird keine Haftung \xC3\xBCbernommen.
