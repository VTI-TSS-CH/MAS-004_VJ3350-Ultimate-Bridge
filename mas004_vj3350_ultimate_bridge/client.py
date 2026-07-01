from __future__ import annotations

import socket
import threading

from .protocol import build_command, parse_result


class UltimateBridgeClient:
    def __init__(self, host: str, port: int, timeout_s: float = 2.0):
        self.host = (host or "").strip()
        self.port = int(port or 0)
        self.timeout_s = float(timeout_s)
        self._lock = threading.RLock()
        self._sock: socket.socket | None = None
        self._connect_count = 0
        self._last_error = ""

    def command(self, command: str, args: list[str] | None = None) -> tuple[bool, str, list[str]]:
        if not self.host or self.port <= 0:
            raise RuntimeError("host/port not configured")

        payload = build_command(command, args)
        with self._lock:
            last_error: Exception | None = None
            for _attempt in range(2):
                try:
                    sock = self._ensure_socket()
                    sock.settimeout(self.timeout_s)
                    sock.sendall(payload)
                    raw = _recv_until(sock, b"\r\n")
                    if not raw:
                        raise RuntimeError("Ultimate endpoint empty reply")
                    self._last_error = ""
                    return parse_result(raw)
                except Exception as exc:
                    last_error = exc
                    self._last_error = repr(exc)
                    self.close()
            assert last_error is not None
            raise last_error

    def _ensure_socket(self) -> socket.socket:
        if self._sock is None:
            sock = socket.create_connection((self.host, self.port), timeout=self.timeout_s)
            sock.settimeout(self.timeout_s)
            try:
                sock.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)
            except Exception:
                pass
            try:
                sock.setsockopt(socket.SOL_SOCKET, socket.SO_KEEPALIVE, 1)
            except Exception:
                pass
            self._sock = sock
            self._connect_count += 1
        return self._sock

    def close(self) -> None:
        sock = self._sock
        self._sock = None
        if sock is not None:
            try:
                sock.close()
            except Exception:
                pass

    def diagnostics(self) -> dict[str, object]:
        with self._lock:
            return {
                "host": self.host,
                "port": self.port,
                "connected": self._sock is not None,
                "connect_count": self._connect_count,
                "last_error": self._last_error,
            }


def _recv_until(sock: socket.socket, marker: bytes, limit: int = 65536) -> bytes:
    data = bytearray()
    while len(data) < limit:
        chunk = sock.recv(1024)
        if not chunk:
            break
        data.extend(chunk)
        if marker in data:
            break
    return bytes(data)
