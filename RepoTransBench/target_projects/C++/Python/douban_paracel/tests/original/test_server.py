def test_server_dummy():
    # Simulate a simple server init, just for "compilation"/import testing
    import socket
    hostname = socket.gethostname()
    server_name = str(hostname)
    # Here we just check that getting the hostname works
    assert isinstance(server_name, str)
    assert len(server_name) > 0