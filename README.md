# Simple AES File Encrypt / Decrypt Scripts
_Einfache AES-Datei-Verschlüsselungs-/-Entschlüsselungsskripte_

---

## English

### Features
* Encrypt **and** decrypt every file in a folder (recursively) with **AES-256-GCM**.  
* Password-based key derivation via **Argon2id**.  
* Stand‑alone binaries can be built with **make / PyInstaller**.
* Optional flags create EDR test artefacts like the EICAR file or a ransom note.

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

---

## Deutsch

### Funktionen
* **AES‑256‑GCM** zum Verschlüsseln **und** Entschlüsseln aller Dateien eines Ordners (inkl. Unterordner).  
* Passwortbasierte Schlüsselableitung mit **Argon2id**.  
* Erstellung eigenständiger Binaries per **make / PyInstaller**.
* Optionale Flags erzeugen EDR-Testdateien wie EICAR oder eine Ransom-Note.

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

## Unity Screenshot Example

The `UnityExamples/ScreenshotUploader.cs` script demonstrates how to capture a screenshot in Unity and upload it to a server. Set `uploadUrl` to your MCP endpoint and `llmUrl` if a language model should receive the screenshot. The script can:

1. **Capture & Upload Screenshot** – send the image to `uploadUrl`.
2. **Capture & Send To LLM Directly** – post straight to `llmUrl`.
3. **Capture & Forward via MCP** – upload to `uploadUrl` and include `llmUrl` in the form so your MCP server can forward it to the requesting LLM.

If `autoSendOnStart` is enabled on the component, the screenshot will be captured
and forwarded automatically when the scene starts, giving the LLM immediate
visual context.

The example uses `UnityWebRequest` and logs the server response. Tools typically rely on a similar HTTP request from the client and let the MCP handle forwarding to an LLM. Direct integration with GitHub Copilot isn't possible, but this pattern allows your own backend or LLM service to analyze the project.

### Simple MCP Forwarding Server

Use `MCPExamples/screenshot_forward_server.py` as a lightweight MCP endpoint. It
accepts a screenshot via `POST /upload` and forwards the image to the given
`forward_url`. If none is provided, it checks the environment variable
`DEFAULT_FORWARD_URL` so screenshots can be automatically sent to a fixed LLM
endpoint.

```bash
pip install -r requirements.txt
python3 MCPExamples/screenshot_forward_server.py
```

Set `DEFAULT_FORWARD_URL` before starting the server if you want every
uploaded screenshot to be forwarded automatically:

```bash
export DEFAULT_FORWARD_URL="https://my-llm-server.example/upload"
python3 MCPExamples/screenshot_forward_server.py
```

Point `uploadUrl` in `ScreenshotUploader` to `http://localhost:8000/upload` and
set `llmUrl` to the `forward_url` provided by the MCP. This mirrors how other
tools return data to the chat that triggered them.
