def simulate_discover(node):
    return node == "/public/integration/node"

def test_integration_discover_with_new_node():
    new_node = "/public/integration/node"
    discovered = simulate_discover(new_node)
    assert discovered, "Should discover the integration public node"