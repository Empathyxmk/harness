def test_targetmap_put_and_get_public():
    class TargetMap:
        def __init__(self):
            self._map = dict()
        def put(self, key, val):
            self._map[key] = val
        def get(self, key):
            return self._map.get(key)
    map = TargetMap()
    map.put("/my/path", "targetValue")
    assert map.get("/my/path") == "targetValue"

def test_targetmap_get_non_existing_key_public():
    class TargetMap:
        def __init__(self):
            self._map = dict()
        def get(self, key):
            return self._map.get(key)
    map = TargetMap()
    assert map.get("/no/such/key") is None