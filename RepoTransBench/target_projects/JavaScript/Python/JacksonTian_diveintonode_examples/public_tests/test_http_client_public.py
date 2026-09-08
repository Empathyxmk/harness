import threading
import http.server
import socketserver
import http.client
import time

def test_http_client_public_requests_path_and_receives_diff_body():
    PORT = 23338
    class Handler(http.server.BaseHTTPRequestHandler):
        def do_GET(self):
            if self.path == '/public':
                self.send_response(200)
                self.send_header('Content-Type', 'text/plain')
                self.end_headers()
                self.wfile.write(b'this is a public test\n')
            else:
                self.send_response(404)
                self.end_headers()
        def log_message(self, format, *args):
            pass  # suppress output

    server = socketserver.TCPServer(('127.0.0.1', PORT), Handler)
    t = threading.Thread(target=server.serve_forever)
    t.start()
    try:
        time.sleep(0.05)
        conn = http.client.HTTPConnection('127.0.0.1', PORT)
        conn.request('GET', '/public')
        resp = conn.getresponse()
        body = resp.read().decode("utf-8")
        assert 'public test' in body
    finally:
        server.shutdown()
        t.join()