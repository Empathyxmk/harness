def test_target_constructors_and_equals():
    class Target:
        def __init__(self, route, target_class):
            self.route = route
            self.target_class = target_class
        def __eq__(self, other):
            if not isinstance(other, Target):
                return False
            return self.route == other.route and self.target_class == other.target_class
        def __hash__(self):
            return hash((self.route, self.target_class))
    t1 = Target("route", "activity")
    t2 = Target("route", "activity")
    t3 = Target("route2", "activity")
    assert t1.route == "route"
    assert t1.target_class == "activity"
    assert t1 == t2
    assert t1 != t3
    assert t1 != None
    assert t1 != object()
    assert hash(t1) == hash(t2)