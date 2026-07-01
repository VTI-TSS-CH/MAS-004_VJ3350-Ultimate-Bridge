import socket
import threading
import unittest

from mas004_vj3350_ultimate_bridge.client import UltimateBridgeClient


class _UltimateLineServer:
    def __init__(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.bind(("127.0.0.1", 0))
        self.sock.listen(8)
        self.host, self.port = self.sock.getsockname()
        self.closed = threading.Event()
        self.connection_count = 0
        self.thread = threading.Thread(target=self._run, daemon=True)
        self.thread.start()

    def close(self):
        self.closed.set()
        try:
            socket.create_connection((self.host, self.port), timeout=0.2).close()
        except Exception:
            pass
        self.thread.join(timeout=1.0)
        self.sock.close()

    def _run(self):
        while not self.closed.is_set():
            try:
                conn, _ = self.sock.accept()
            except OSError:
                return
            self.connection_count += 1
            threading.Thread(target=self._serve_client, args=(conn,), daemon=True).start()

    def _serve_client(self, conn):
        with conn:
            while not self.closed.is_set():
                data = bytearray()
                while b"\r\n" not in data:
                    chunk = conn.recv(1024)
                    if not chunk:
                        return
                    data.extend(chunk)
                conn.sendall(b"\x06OK;VALUE\r\n")


class UltimateBridgeClientTests(unittest.TestCase):
    def test_command_reuses_socket(self):
        server = _UltimateLineServer()
        client = UltimateBridgeClient(server.host, server.port, timeout_s=1.0)
        try:
            self.assertTrue(client.command("GetVersion")[0])
            self.assertTrue(client.command("GetVersion")[0])
            self.assertEqual(1, server.connection_count)
            self.assertTrue(client.diagnostics()["connected"])
        finally:
            client.close()
            server.close()


if __name__ == "__main__":
    unittest.main()
