# Simple AES File Encrypt/Decrypt Scripts

## English

**Encrypt and decrypt all files in a folder (including subfolders) with AES-256-GCM.**

### Requirements

- Python 3.x
- Install [PyCryptodome](https://www.pycryptodome.org/) and [argon2-cffi](https://pypi.org/project/argon2-cffi/):
  ```
  pip3 install -r requirements.txt
  ```

- Run either
### Usage
#### 1. Encrypt
#### 2. Decrypt

### Notes
### Disclaimer

## Deutsch

**Verschl\xC3\xBCssle und entschl\xC3\xBCssle alle Dateien in einem Ordner (inkl. Unterordner) mit AES-256-GCM.**

### Voraussetzungen

- Python 3.x
- [PyCryptodome](https://www.pycryptodome.org/) und [argon2-cffi](https://pypi.org/project/argon2-cffi/) installieren:
  ```
  pip3 install -r requirements.txt
  ```

### Kompilierte Version

- `make` erzeugt eigenst\xC3\xA4ndige Binaries im Verzeichnis `bin/`.
- Das Skript `compile.sh` installiert die Abh\xC3\xA4ngigkeiten und ruft danach `make` auf.
- F\xC3\xBChre also entweder
  ```
  make
  ```
  oder
  ```
  ./compile.sh
  ```
  aus.
- Danach findest du die Ausf\xC3\xBChrbaren Dateien in `bin/`. Mit `make clean` werden die Build-Dateien entfernt.

### Verwendung

#### 1. Verschl\xC3\xBCsseln

- Passe `START_PATH` in `encrypt_all.py` an dein Zielverzeichnis an.
- Starte das Skript und gib eine Passphrase ein:
  ```
  python3 encrypt_all.py
  ```
- Die Passphrase wird mittels Argon2id in einen Schl\xC3\xBCssel abgeleitet.
- Parameter wie Salz und Zeit-/Speicherkosten werden in `MOCKBIT_KEY.txt` gespeichert.
- Alle Dateien werden als `.mock` verschl\xC3\xBCsselt, die Originale werden sicher gel\xC3\xB6scht.
- Der erzeugte BASE64-Schl\xC3\xBCssel wird angezeigt – **unbedingt sichern!**

#### 2. Entschl\xC3\xBCsseln

- Passe `START_PATH` in `decrypt_all.py` an das Verzeichnis mit den `.mock`-Dateien an.
- Stelle sicher, dass `MOCKBIT_KEY.txt` vorhanden ist und gib dieselbe Passphrase ein.
- Starte das Skript:
  ```
  python3 decrypt_all.py
  ```
- Die Dateien werden wiederhergestellt, `.mock`-Dateien werden entfernt.

### Hinweise

- **Unbedingt zuerst in einer Testumgebung ausprobieren!**
- Ohne den Schl\xC3\xBCssel kann niemand die Daten wiederherstellen.
- Beim Entschl\xC3\xBCsseln werden vorhandene Dateien nicht \xC3\xBCberschrieben; sie erhalten ihren urspr\xC3\xBCnglichen Namen zur\xC3\xBCck.
- F\xC3\xBCr Backups oder produktiven Einsatz bitte weiterentwickeln!

### Haftungsausschluss

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

- Passe `START_PATH` in `decrypt_all.py` auf das Verzeichnis mit den `.mock`-Dateien an.
- Stelle sicher, dass `MOCKBIT_KEY.txt` dort liegt und gib dieselbe Passphrase ein.
- Starte das Skript:
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
