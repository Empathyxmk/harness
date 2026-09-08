# Simulating IO Monad pattern test - original
class IO:
    def __init__(self, effect):
        self.effect = effect
    def map(self, f):
        return IO(lambda: f(self.effect()))
    def run(self):
        return self.effect()

def test_io_map_returns_new_io():
    io = IO(lambda: 2)
    incremented = io.map(lambda x: x + 1)
    assert io.run() == 2
    assert incremented.run() == 3

def test_io_chain_effects():
    io1 = IO(lambda: 3)
    io2 = io1.map(lambda x: x * 10)
    io3 = io2.map(str)
    assert io1.run() == 3
    assert io2.run() == 30
    assert io3.run() == "30"