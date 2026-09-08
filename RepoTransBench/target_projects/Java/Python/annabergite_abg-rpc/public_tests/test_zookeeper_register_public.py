def do_register(znode):
    return "/register/public/" in znode

def test_register_new_path():
    znode = "/register/public/node"
    registered = do_register(znode)
    assert registered, "Should register public node"