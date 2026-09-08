def test_inner_class_access_public_variant():
    class OuterClassPublic:
        def __init__(self, value):
            self._value = value

        class InnerClass:
            def __init__(self, outer):
                self._outer = outer
            def multiplyOuterField(self, by):
                return self._outer._value * by

    outer = OuterClassPublic(21)
    inner = OuterClassPublic.InnerClass(outer)
    assert inner.multiplyOuterField(5) == 105