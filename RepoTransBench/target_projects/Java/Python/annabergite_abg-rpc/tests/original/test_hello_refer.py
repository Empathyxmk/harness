class HelloService:
    def hello(self, msg):
        return f"Hello {msg}"

class HelloReferTest:
    def __init__(self):
        self.helloService = HelloService()

    def doSomeThing(self, msg):
        result = self.helloService.hello(msg)
        # Normally would call thenAccept -- here just check result
        return result

def test_hello_refer_dosomething():
    obj = HelloReferTest()
    res = obj.doSomeThing("World")
    assert res == "Hello World"