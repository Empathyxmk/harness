def simulate_server_start(server_id, port):
    return f"KCP Public Test Server Started (ServerID: {server_id}, Port: {port})"

def test_simple_public_server():
    server_id = 42
    port = 16667
    expected_greeting = "KCP Public Test Server Started (ServerID: 42, Port: 16667)"
    server_greeting = simulate_server_start(server_id, port)
    assert server_greeting == expected_greeting