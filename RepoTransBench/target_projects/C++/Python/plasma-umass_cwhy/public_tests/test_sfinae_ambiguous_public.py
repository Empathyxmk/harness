class WithType:
    class type:
        pass

class WithoutType:
    pass

def f(obj):
    if hasattr(obj, 'type'):
        # Simulate "with type" overload
        return 0
    else:
        return 1.5

def test_sfinae_with_type():
    result_with = f(WithType())
    assert result_with == 0

def test_sfinae_without_type():
    result_without = f(WithoutType())
    assert result_without == 1.5