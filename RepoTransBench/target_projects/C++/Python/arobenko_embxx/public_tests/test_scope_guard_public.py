def scope_guard(callback):
    class Guard:
        def __init__(self, cb):
            self.cb = cb
            self.active = True
        def release(self):
            self.active = False
        def __enter__(self):
            return self
        def __exit__(self, exc_type, exc_val, exc_tb):
            if self.active:
                self.cb()
            return False
        def __del__(self):
            if getattr(self, "active", False):
                self.__exit__(None, None, None)
    return Guard(callback)

def test_public_basic_guard():
    result = {"value": 11}
    guard = scope_guard(lambda: result.update(value=result["value"] + 23))
    assert result["value"] == 11
    del guard

def test_public_resource_guard():
    status = {"value": 6}
    guard = None
    def cb():
        status["value"] = status["value"] * 4
    with scope_guard(cb):
        assert status["value"] == 6
    assert status["value"] == 24