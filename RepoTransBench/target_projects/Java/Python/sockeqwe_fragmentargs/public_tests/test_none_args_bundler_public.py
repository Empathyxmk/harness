from tests.original.test_none_args_bundler import NoneArgsBundler, Bundle

def test_public_test_instance_singleton():
    a = NoneArgsBundler.get()
    b = NoneArgsBundler.get()
    assert a is b

def test_public_test_put_null_always():
    assert NoneArgsBundler.get().put("publicKey", "hello", Bundle()) is None

def test_public_test_get_null_always():
    assert NoneArgsBundler.get().get("anotherKey", Bundle()) is None