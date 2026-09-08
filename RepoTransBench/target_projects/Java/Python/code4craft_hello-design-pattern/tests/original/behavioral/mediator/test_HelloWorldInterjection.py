def test_DefaultConstructorAndSetter():
    class HelloWorldInterjection:
        def __init__(self):
            pass
    inter = HelloWorldInterjection()
    assert inter is not None