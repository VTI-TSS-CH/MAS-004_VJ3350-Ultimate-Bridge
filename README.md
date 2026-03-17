# MAS-004_VJ3350-Ultimate-Bridge

Basis-Client und Daemon fuer Videojet 3350 ueber Ultimate-Protokoll.

## Python fuer Schulung und Entwicklung
- Teamstandard fuer neue Entwicklungsrechner: `Python 3.13.x`
- `Python 3.12.x` ist als Fallback okay, wenn `3.13` auf dem Zielsystem nicht sauber verfuegbar ist
- `Python 3.14` derzeit nicht als Schulungsstandard verwenden
- `requires-python = ">=3.9"` im `pyproject.toml` beschreibt nur die technische Mindestversion, nicht die empfohlene Teamversion

## Protokoll
- UTF-8 Text
- Delimiter `;`
- Ende `CRLF`
- Antwort startet mit `ACK` (0x06) oder `NAK` (0x15)

## Service-Dateien
- `systemd/mas004-vj3350-ultimate-bridge.service`
- `scripts/install.sh`
- `scripts/run.sh`
- `scripts/default_config.json`

## Installation auf Raspi
```bash
cd /opt/MAS-004_VJ3350-Ultimate-Bridge
python3.13 -m venv .venv
# alternativ auf Systemen ohne 3.13: python3.12 -m venv .venv
source .venv/bin/activate
pip install -U pip
pip install -e .
chmod +x scripts/*.sh
./scripts/install.sh
```

## Config
`/etc/mas004_vj3350_ultimate_bridge/config.json`

- `enabled`: Service aktiv/inaktiv
- `simulation`: wenn `true`, keine Live-Verbindung
- `host`, `port`: Laser Endpoint
- `probe_command`: Default `GetVersion`
- `timeout_s`, `poll_interval_s`
