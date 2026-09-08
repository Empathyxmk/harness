def test_targetmap_put_and_get():
    class Target:
        def __init__(self, route, target_class):
            self.route = route
            self.target_class = target_class
        def __eq__(self, other):
            return isinstance(other, Target) and self.route == other.route and self.target_class == other.target_class
    class TargetMap:
        def __init__(self):
            self._map = dict()
        def put(self, key, val):
            self._map[key] = val
        def contains_key(self, key):
            return key in self._map
        def get(self, key):
            return self._map.get(key)
        def remove(self, key):
            if key in self._map:
                del self._map[key]
        def is_empty(self):
            return not self._map
    map = TargetMap()
    t1 = Target("route1", "activity1")
    map.put("key", t1)
    assert map.contains_key("key")
    assert map.get("key") == t1

def test_targetmap_remove():
    class Target:
        def __init__(self, route, target_class):
            self.route = route
            self.target_class = target_class
        def __eq__(self, other):
            return isinstance(other, Target) and self.route == other.route and self.target_class == other.target_class
    class TargetMap:
        def __init__(self):
            self._map = dict()
        def put(self, key, val):
            self._map[key] = val
        def contains_key(self, key):
            return key in self._map
        def get(self, key):
            return self._map.get(key)
        def remove(self, key):
            if key in self._map:
                del self._map[key]
        def is_empty(self):
            return not self._map
    map = TargetMap()
    t1 = Target("route2", "activity2")
    map.put("rm", t1)
    map.remove("rm")
    assert map.contains_key("rm") is False

def test_targetmap_is_empty():
    class Target:
        def __init__(self, route, target_class):
            self.route = route
            self.target_class = target_class
        def __eq__(self, other):
            return isinstance(other, Target) and self.route == other.route and self.target_class == other.target_class
    class TargetMap:
        def __init__(self):
            self._map = dict()
        def put(self, key, val):
            self._map[key] = val
        def contains_key(self, key):
            return key in self._map
        def get(self, key):
            return self._map.get(key)
        def remove(self, key):
            if key in self._map:
                del self._map[key]
        def is_empty(self):
            return not self._map
    map = TargetMap()
    assert map.is_empty()
    map.put("a", Target("a", "a"))
    map.remove("a")
    assert map.is_empty()