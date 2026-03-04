# SUPPORT_RUNBOOK - MAS-004_VJ3350-Ultimate-Bridge

## 1. Positioning
- Subproject, operationally subordinate to `MAS-004_RPI-Databridge`.

## 2. Local Setup
- `python -m venv .venv`
- `.\.venv\Scripts\Activate.ps1`
- `python -m pip install -U pip`
- `python -m pip install -e .`

## 3. Pi Deployment
- Pull:
  - `ssh mas004-rpi "cd /opt/MAS-004_VJ3350-Ultimate-Bridge && git pull --ff-only"`
- Restart:
  - `ssh mas004-rpi "sudo systemctl restart mas004-vj3350-ultimate-bridge.service"`
- Logs:
  - `ssh mas004-rpi "sudo journalctl -u mas004-vj3350-ultimate-bridge.service -n 120 --no-pager"`

## 4. Verification
- Service active.
- `host`/`port`/`probe_command` values valid.
- Probe transitions are stable (`probe ok` vs `probe NAK`/errors).

## 5. Sync Rule
- Use main repo scripts:
  - `MAS-004_RPI-Databridge/scripts/mas004_multirepo_status.ps1`
  - `MAS-004_RPI-Databridge/scripts/mas004_multirepo_sync.ps1`
- Keep Pi dirty working trees untouched unless explicitly resolved.
