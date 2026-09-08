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
def test_tls_client_public_connects_to_server_and_pipes_different_data(tmp_path):
    # This public test uses a different port and message
    KEYSDIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "../tls/keys")
    cert_file = os.path.join(KEYSDIR, 'server.crt')
    key_file = os.path.join(KEYSDIR, 'server.key')
    ca_file = os.path.join(KEYSDIR, 'ca.crt')
    client_cert_file = os.path.join(KEYSDIR, 'client.crt')
    client_key_file = os.path.join(KEYSDIR, 'client.key')
    host, port = '127.0.0.1', 18013

    context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
    context.load_cert_chain(certfile=cert_file, keyfile=key_file)
    context.load_verify_locations(cafile=ca_file)
    context.verify_mode = ssl.CERT_REQUIRED

    client_context = ssl.create_default_context(ssl.Purpose.SERVER_AUTH)
    client_context.load_cert_chain(certfile=client_cert_file, keyfile=client_key_file)
    client_context.load_verify_locations(cafile=ca_file)
    client_context.check_hostname = False
    client_context.verify_mode = ssl.CERT_NONE

    def server_fun():
        with socket.socket() as sock:
            sock.bind((host, port))
            sock.listen(1)
            with context.wrap_socket(sock, server_side=True) as ssock:
                conn, addr = ssock.accept()
                with conn:
                    data = conn.recv(1024)
                    conn.send(b"hello-public!\n")
                    time.sleep(0.05)

    server_thread = threading.Thread(target=server_fun)
    server_thread.start()
    time.sleep(0.05)
    client_logs = []
    with socket.create_connection((host, port), timeout=3) as raw_sock:
        with client_context.wrap_socket(raw_sock, server_hostname=host) as client_sock:
            client_logs.append("client connected")
            client_sock.send(b"Hello from PUBLIC client!\n")
            received = client_sock.recv(1024).decode("utf-8")
            assert "hello-public!" in received
            assert any("client connected" in l for l in client_logs)
    server_thread.join()