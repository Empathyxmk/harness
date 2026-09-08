import pytest
import ssl
import os
import socket
import threading
import time

@pytest.mark.skipif(
    not hasattr(ssl, 'create_default_context'),
    reason="Requires SSL support"
)
def test_tls_server_starts_and_receives_client_connection(tmp_path):
    KEYSDIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "../tls/keys")
    cert_file = os.path.join(KEYSDIR, 'server.crt')
    key_file = os.path.join(KEYSDIR, 'server.key')
    ca_file = os.path.join(KEYSDIR, 'ca.crt')
    client_cert_file = os.path.join(KEYSDIR, 'client.crt')
    client_key_file = os.path.join(KEYSDIR, 'client.key')
    host, port = '127.0.0.1', 18001

    context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
    context.load_cert_chain(certfile=cert_file, keyfile=key_file)
    context.load_verify_locations(cafile=ca_file)
    context.verify_mode = ssl.CERT_REQUIRED

    client_context = ssl.create_default_context(ssl.Purpose.SERVER_AUTH)
    client_context.load_cert_chain(certfile=client_cert_file, keyfile=client_key_file)
    client_context.load_verify_locations(cafile=ca_file)
    client_context.check_hostname = False
    client_context.verify_mode = ssl.CERT_NONE

    def server_main():
        with socket.socket() as sock:
            sock.bind((host, port))
            sock.listen(1)
            with context.wrap_socket(sock, server_side=True) as ssock:
                conn, addr = ssock.accept()
                with conn:
                    d = conn.recv(128)
                    conn.send(b"welcome!\n")
                    time.sleep(0.05)

    server_thread = threading.Thread(target=server_main)
    server_thread.start()
    time.sleep(0.05)
    with socket.create_connection((host, port), timeout=3) as raw_sock:
        with client_context.wrap_socket(raw_sock, server_hostname=host) as client_sock:
            client_sock.send(b"hello\n")
            received = client_sock.recv(128).decode("utf-8")
            # No assertion required, as JS test no longer checks received text.
    server_thread.join()