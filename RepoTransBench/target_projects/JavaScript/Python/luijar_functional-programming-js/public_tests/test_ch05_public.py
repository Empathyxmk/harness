# Simulating IO Monad usage - public
class IO:
    def __init__(self, effect):
        self.effect = effect
    def map(self, f):
        return IO(lambda: f(self.effect()))
    def run(self):
        return self.effect()

def test_public_io_simple_map():
    io = IO(lambda: 10)
    plus = io.map(lambda x: x+5)
    assert plus.run() == 15

def test_public_io_identity():
    io = IO(lambda: "hello")
    same = io.map(lambda x: x)
    assert same.run() == "hello"