# PROJECT_CONTEXT - MAS-004_VJ3350-Ultimate-Bridge

## Role in MAS-004
- Subproject (not orchestration owner).
- Provides Videojet 3350 connectivity using Ultimate protocol.
- Intended to be consumed by `MAS-004_RPI-Databridge` for production integration.

## Repository Scope
- Package: `mas004_vj3350_ultimate_bridge/`
- Protocol parser/builder: `protocol.py`
- TCP client: `client.py`
- Probe loop/service: `service.py`
- Config model: `config.py`

## Protocol Summary
- UTF-8 text with `;` delimiters and `CRLF` line ending.
- Response starts with ACK (`0x06`) or NAK (`0x15`).

## Runtime Paths
- Config: `/etc/mas004_vj3350_ultimate_bridge/config.json`
- Systemd unit: `mas004-vj3350-ultimate-bridge.service`
- Pi repo path: `/opt/MAS-004_VJ3350-Ultimate-Bridge`

## Integration Boundary
- This repo should expose stable transport/probe behavior.
- Main Databridge remains responsible for parameter policy/routing.

## Last Reviewed
- Date: 2026-03-04
- Local HEAD baseline during creation: `4928fd3`
