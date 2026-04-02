import json
from http.server import BaseHTTPRequestHandler, HTTPServer
from threading import Thread

from runtime.mcp.registry import ManagedMCPRegistry
from runtime.mcp.session_host import ManagedMCPSessionHost


class _OkHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"ok")

    def log_message(self, format, *args):
        return


def test_managed_mcp_session_host_probes_endpoint(tmp_path):
    server = HTTPServer(("127.0.0.1", 0), _OkHandler)
    thread = Thread(target=server.serve_forever, daemon=True)
    thread.start()

    config_path = tmp_path / "managed-mcp.json"
    config_path.write_text(
        json.dumps(
            [
                {
                    "name": "local-managed",
                    "transport": "http",
                    "url": f"http://127.0.0.1:{server.server_port}/health",
                    "env": {},
                }
            ]
        ),
        encoding="utf-8",
    )

    registry = ManagedMCPRegistry(config_path)
    registry.load()
    host = ManagedMCPSessionHost(registry)
    session = host.connect("local-managed")
    server.shutdown()

    assert session.connected is True
    assert session.status_code == 200


def test_managed_mcp_session_host_writes_report(tmp_path):
    config_path = tmp_path / "managed-mcp.json"
    config_path.write_text(
        '[{"name":"offline","transport":"http","url":"http://127.0.0.1:1/","env":{}}]',
        encoding="utf-8",
    )

    registry = ManagedMCPRegistry(config_path)
    registry.load()
    host = ManagedMCPSessionHost(registry)
    host.connect("offline", timeout_seconds=0.01)

    report_path = host.write_report(tmp_path / "report.yaml")
    assert report_path.exists()
    assert "sessions:" in report_path.read_text(encoding="utf-8")
