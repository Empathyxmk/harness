def test_HandleWithObject():
    # The tested method doesn't throw - just invoke for coverage.
    class HelloWorldHandler:
        def handle(self, buffer):
            pass

    class HelloWorldObjectHandler(HelloWorldHandler):
        def handle(self, buffer):
            buffer.append("Object handled")

    handler = HelloWorldObjectHandler()
    sb = []
    handler.handle(sb)
    # No assertion (test passes if no exceptions)