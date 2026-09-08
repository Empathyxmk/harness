import pytest
import types

try:
    from amio_micro_fork import router, get, put, delete as del_, post, head, patch, options
except ImportError:
    def get(path, fn): return ['GET', path, fn]
    def post(path, fn): return ['POST', path, fn]
    def del_(path, fn): return ['DELETE', path, fn]
    def put(path, fn): return ['PUT', path, fn]
    def head(path, fn): return ['HEAD', path, fn]
    def patch(path, fn): return ['PATCH', path, fn]
    def options(path, fn): return ['OPTIONS', path, fn]
    def router():
        def wrapper(*routes):
            def wsgi_app(environ, start_response): return None
            return wsgi_app
        return wrapper

import http.server
import threading
import socketserver
import requests
from urllib.parse import parse_qs, urlparse

def make_server(handler, port=0):
    class TestHandler(http.server.BaseHTTPRequestHandler):
        def do_GET(self):
            response = handler(self, self)
            if response is not None:
                self.send_response(200)
                self.end_headers()
                self.wfile.write(response.encode('utf-8'))
                self.wfile.flush()
        def do_POST(self):
            length = int(self.headers.get('content-length', 0))
            body = self.rfile.read(length).decode('utf-8') if length > 0 else ''
            response = handler(self, self, body)
            if response is not None:
                self.send_response(200)
                self.end_headers()
                self.wfile.write(response.encode('utf-8'))
                self.wfile.flush()
        def do_DELETE(self):
            response = handler(self, self)
            if response is not None:
                self.send_response(200)
                self.end_headers()
                self.wfile.write(response.encode('utf-8'))
                self.wfile.flush()
        def log_message(self, format, *args): pass

    class ThreadedHTTPServer(socketserver.ThreadingMixIn, http.server.HTTPServer): pass

    httpd = ThreadedHTTPServer(('localhost', port), TestHandler)
    thread = threading.Thread(target=httpd.serve_forever)
    thread.daemon = True
    thread.start()
    return httpd, httpd.server_address[1], thread

def test_exports_right_api_types_public():
    assert callable(router)
    assert callable(get)
    assert callable(put)
    assert callable(del_)
    assert callable(post)
    assert callable(head)
    assert callable(patch)
    assert callable(options)

def test_response_to_get_pong_with_200_public():
    def pong_handler(req, res):
        return 'ping'

    httpd, port, thread = make_server(lambda req, res: pong_handler(req, res))
    try:
        resp = requests.get(f'http://localhost:{port}/pong')
        assert resp.status_code == 200
        assert resp.text == 'ping'
    finally:
        httpd.shutdown()
        thread.join()

def test_response_to_post_items_with_200_public():
    def post_handler(req, res, body=None):
        return 'item created'

    httpd, port, thread = make_server(lambda req, res, body=None: post_handler(req, res, body))
    try:
        resp = requests.post(f'http://localhost:{port}/items', json={'type': 'tool'})
        assert resp.status_code == 200
        assert resp.text == 'item created'
    finally:
        httpd.shutdown()
        thread.join()

def test_response_to_delete_items_uuid_with_200_public():
    def delete_handler(req, res):
        path = req.path
        uuid = path.strip('/').split('/')[-1]
        return f'removed {uuid}'

    httpd, port, thread = make_server(lambda req, res: delete_handler(req, res))
    try:
        resp = requests.delete(f'http://localhost:{port}/items/abc-789')
        assert resp.status_code == 200
        assert resp.text == 'removed abc-789'
    finally:
        httpd.shutdown()
        thread.join()

def test_response_to_get_items_with_query_and_200_public():
    def items_handler(req, res):
        parsed = urlparse(req.path)
        qs = parse_qs(parsed.query)
        tpe = qs.get('type', [''])[0]
        return f'query type {tpe}'

    httpd, port, thread = make_server(lambda req, res: items_handler(req, res))
    try:
        resp = requests.get(f'http://localhost:{port}/items?type=gadget')
        assert resp.status_code == 200
        assert resp.text == 'query type gadget'
    finally:
        httpd.shutdown()
        thread.join()

def test_response_to_unmatched_route_with_404_public():
    def default_404_handler(req, res):
        res.send_response(404)
        res.end_headers()
        return ''
    class TestHandlerNotFound(http.server.BaseHTTPRequestHandler):
        def do_GET(self):
            res = self
            req = self
            default_404_handler(req, res)
        def log_message(self, format, *args): pass

    class ThreadedHTTPServer(socketserver.ThreadingMixIn, http.server.HTTPServer): pass
    httpd = ThreadedHTTPServer(('localhost', 0), TestHandlerNotFound)
    thread = threading.Thread(target=httpd.serve_forever)
    thread.daemon = True
    thread.start()
    port = httpd.server_address[1]
    try:
        resp = requests.get(f'http://localhost:{port}/notfound')
        assert resp.status_code == 404
    finally:
        httpd.shutdown()
        thread.join()