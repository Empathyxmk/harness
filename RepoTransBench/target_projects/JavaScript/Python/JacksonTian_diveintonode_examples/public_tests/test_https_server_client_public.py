import ssl
import os
import socket
import threading
import time

def test_https_server_public_responds_to_https_client_with_diff_output(tmp_path):
    KEYSDIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "../https/keys")
    cert_file = os.path.join(KEYSDIR, 'server.crt')
    key_file = os.path.join(KEYSDIR, 'server.key')
    client_cert_file = os.path.join(KEYSDIR, 'client.crt')
    client_key_file = os.path.join(KEYSDIR, 'client.key')
    host, port = '127.0.0.1', 18012

    server_context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
    server_context.load_cert_chain(certfile=cert_file, keyfile=key_file)

    client_context = ssl.create_default_context(ssl.Purpose.SERVER_AUTH)
    client_context.load_cert_chain(certfile=client_cert_file, keyfile=client_key_file)
    client_context.check_hostname = False
    client_context.verify_mode = ssl.CERT_NONE

    def server_fun():
        with socket.socket() as sock:
            sock.bind((host, port))
            sock.listen(1)
            with server_context.wrap_socket(sock, server_side=True) as ssock:
                conn, addr = ssock.accept()
                with conn:
                    req = conn.recv(1024)
                    conn.sendall(
                        b"HTTP/1.1 200 OK\r\n"
                        b"Content-Type: text/plain\r\n"
                        b"Content-Length: 19\r\n"
                        b"\r\n"
                        b"hello PUBLIC test!\n"
                    )

    server_thread = threading.Thread(target=server_fun)
    server_thread.start()
    time.sleep(0.05)
    with socket.create_connection((host, port), timeout=3) as raw_sock:
        with client_context.wrap_socket(raw_sock, server_hostname=host) as client_sock:
            req = (
                b"GET / HTTP/1.1\r\n"
                b"Host: localhost\r\n"
                b"\r\n"
            )
            client_sock.send(req)
            resp = b""
            while True:
                chunk = client_sock.recv(4096)
                if not chunk:
                    break
                resp += chunk
                if b"hello PUBLIC test!\n" in resp:
                    break
            assert b"hello PUBLIC test!" in resp
    server_thread.join()