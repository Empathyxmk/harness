import threading
import http.server
import socketserver
import http.client
import time

def test_client_gets_response_and_logs():
    # Setup minimal HTTP server (runs in background thread)
    PORT = 1337
    responses = {}
    class Handler(http.server.BaseHTTPRequestHandler):
        def do_GET(self):
            self.send_response(200)
            self.send_header('X-Test', 'ok')
            self.end_headers()
            self.wfile.write(b'testdata')
        def log_message(self, format, *args):
            pass  # suppress logging

    server = socketserver.TCPServer(('127.0.0.1', PORT), Handler)
    t = threading.Thread(target=server.serve_forever)
    t.start()
    try:
        time.sleep(0.05)
        logs = []
        conn = http.client.HTTPConnection('127.0.0.1', PORT)
        conn.request('GET', '/')
        resp = conn.getresponse()
        logs.append('STATUS: %d' % resp.status)
        logs.append('HEADERS: %s' % dict(resp.getheaders()))
        chunked = resp.read().decode("utf-8")
        assert any('STATUS: 200' in l for l in logs)
        assert any('HEADERS' in l for l in logs)
        assert chunked == 'testdata'
    finally:
        server.shutdown()
        t.join()