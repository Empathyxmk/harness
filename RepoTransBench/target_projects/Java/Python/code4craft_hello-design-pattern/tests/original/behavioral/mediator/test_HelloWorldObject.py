def test_DefaultConstructor():
    class HelloWorldObject:
        def __init__(self):
            pass
    obj = HelloWorldObject()
    assert obj is not None