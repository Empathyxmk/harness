class Feather:
    def inject_fields(self, target):
        # naive simulation: inject attribute 'a' if present and None
        if hasattr(target, "a") and getattr(target, "a") is None:
            setattr(target, "a", A())

class Target:
    def __init__(self):
        self.a = None

class A:
    pass

def test_fields_injected():
    feather = Feather()
    target = Target()
    feather.inject_fields(target)
    assert target.a is not None