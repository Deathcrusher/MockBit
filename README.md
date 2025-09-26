# Simple AES File Encrypt / Decrypt Scripts
_Einfache AES-Datei-Verschlüsselungs-/-Entschlüsselungsskripte_

---

## English

### Features
* Encrypt **and** decrypt every file in a folder (recursively) with **AES-256-GCM**.  
* Password-based key derivation via **Argon2id**.  
* Stand‑alone binaries can be built with **make / PyInstaller**.
* Optional flags create EDR test artefacts like a ransom note.

### Requirements
* Python 3.8+  
* [PyCryptodome](https://www.pycryptodome.org/)  
* [argon2-cffi](https://pypi.org/project/argon2-cffi/)

```bash
pip3 install -r requirements.txt
```

### Building Stand‑Alone Binaries

```bash
make          # just build
./compile.sh  # install deps & build
```

`compile.sh` creates `~/tmp` and sets `TMPDIR` automatically so the build works
on systems where `/tmp` is mounted with `noexec`. If you run the scripts
directly, export `TMPDIR=$HOME/tmp` yourself.

The binaries are placed in **bin/**.  
Run `make clean` to remove build artefacts.

### Usage

| Step | Action | Command / Notes |
|------|--------|-----------------|
| 1 | **Encrypt** | `python3 encrypt_all.py --path folder` (add `--time`, `--memory`, `--parallelism`, `--ransom-sim`, `--ransom-note` if needed)<br>Enter passphrase → key derived via Argon2id<br>Salt & Argon2 params saved to **MOCKBIT_KEY.txt**<br>Original files deleted, encrypted copies end with **.mock** |
| 2 | **Decrypt** | `python3 decrypt_all.py --path folder` (same optional parameters)<br>Enter the same passphrase → files are restored, `.mock` files removed |

### Notes
* **Always test in a safe environment first.**
* Without the key, the data is unrecoverable.
* Existing files are never overwritten on decrypt.
* Extend the scripts for backups or production use as needed.

### Disclaimer
Use at your own risk. No liability for data loss or misuse.

### 🧪 Ransomware-Simulation Mode
Enable via `--ransom-sim` and optional `--sim-path` (defaults to `./testdata`). The tool XOR-encrypts files to `<name>.mocklock`, writes a ransom note and echoes a fake backup wipe. This helps EDR or XDR solutions detect malicious activity. The encryption key is always 0xAA so data can be restored. Run only in disposable test directories. To undo the simulation, run `python3 decrypt_all.py --ransom-sim --sim-path <dir>` on the same directory.

### Linux Payload for EDR Testing
`python3 -m mockbit.linux_payload --path folder` runs the ransomware simulation
on *folder*. This makes it easy for EDR solutions to spot malicious behaviour.
Execute only in safe test environments.

#### Triggering the payload remotely (example)

If you manage the test machine from a central controller, you can point the
payload at a specific directory through an environment variable and run it over
SSH. The controller only forwards the command; **the encryption routine runs on
the victim host** because the shell opened by `ssh` executes there. You can
verify this by prefacing the command with `hostname`—the printed name will be
the victim, not the controller.

```bash
TARGET_DIR=/safe/test/directory
ssh edr-lab "hostname && TARGET_DIR=$TARGET_DIR python3 -m mockbit.linux_payload --path \"$TARGET_DIR\""
```

The `TARGET_DIR` variable is expanded by the remote shell, so the victim system
receives the correct path and encrypts only that directory in simulation mode.
Adjust usernames, hostnames, and the folder path to match your lab setup.

Alternatively, log on to the victim machine (via SSH or console), export the
target directory locally, and run the payload directly to ensure the
instrumentation sees the activity as originating from that host:

```bash
ssh edr-lab
export TARGET_DIR=/safe/test/directory
python3 -m mockbit.linux_payload --path "$TARGET_DIR"
```

Both workflows execute the payload entirely on the victim.

---

## Deutsch

### Funktionen
* **AES‑256‑GCM** zum Verschlüsseln **und** Entschlüsseln aller Dateien eines Ordners (inkl. Unterordner).  
* Passwortbasierte Schlüsselableitung mit **Argon2id**.  
* Erstellung eigenständiger Binaries per **make / PyInstaller**.
* Optionale Flags erzeugen EDR-Testdateien wie eine Ransom-Note.

### Voraussetzungen
* Python 3.8+  
* [PyCryptodome](https://www.pycryptodome.org/)  
* [argon2-cffi](https://pypi.org/project/argon2-cffi/)

```bash
pip3 install -r requirements.txt
```

### Kompilierte Version bauen

```bash
make          # nur bauen
./compile.sh  # Abhängigkeiten installieren und bauen
```

`compile.sh` legt automatisch `~/tmp` an und setzt `TMPDIR`, falls `/tmp` mit
`noexec` eingehängt ist. Wenn du die Skripte direkt aufrufst, setze
`TMPDIR=$HOME/tmp` selbst.

Die Binaries liegen anschließend in **bin/**.  
Mit `make clean` entfernst du die Build-Dateien.

### Verwendung

| Schritt | Aktion | Befehl / Hinweise |
|---------|--------|-------------------|
| 1 | **Verschlüsseln** | `python3 encrypt_all.py --path ordner` (optional `--time`, `--memory`, `--parallelism`, `--ransom-sim`, `--ransom-note`)<br>Passphrase eingeben → Schlüssel wird via Argon2id abgeleitet<br>Salz & Argon2‑Parameter in **MOCKBIT_KEY.txt**<br>Originale werden sicher gelöscht, verschlüsselte Dateien enden auf **.mock** |
| 2 | **Entschlüsseln** | `python3 decrypt_all.py --path ordner` (gleiche optionale Parameter)<br>Dieselbe Passphrase eingeben → Dateien werden wiederhergestellt, `.mock`‑Dateien entfernt |

### Hinweise
* **Unbedingt zuerst in einer Testumgebung ausprobieren.**
* Ohne den Schlüssel kann niemand die Daten wiederherstellen.
* Beim Entschlüsseln werden vorhandene Dateien nicht überschrieben.
* Für Backups oder produktiven Einsatz sind Erweiterungen erforderlich.

### Haftungsausschluss
Benutzung auf eigene Gefahr. Keine Haftung für Datenverlust oder Missbrauch.

### Linux-Payload für EDR-Tests
Mit `python3 -m mockbit.linux_payload --path ordner` wird die
Ransomware-Simulation auf *ordner* ausgeführt. Dies ermöglicht es
EDR-Lösungen, die Aktivität zu erkennen. Nur in sicheren Testumgebungen
ausführen.
