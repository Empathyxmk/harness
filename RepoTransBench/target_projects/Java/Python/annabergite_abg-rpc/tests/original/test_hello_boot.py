class HelloService:
    def hello(self):
        return "Hello!"

class HelloBootTest:
    def __init__(self):
        self.helloService = HelloService()

def test_hello_boot_autowired_service():
    app = HelloBootTest()
    assert app.helloService.hello() == "Hello!"