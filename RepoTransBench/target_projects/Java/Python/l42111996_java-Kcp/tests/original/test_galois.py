import pytest

class Galois:
    @staticmethod
    def add(a, b): return (a + b) % 256
    @staticmethod
    def subtract(a, b): return (a - b) % 256
    @staticmethod
    def multiply(a, b): return (a * b) % 256
    @staticmethod
    def divide(a, b): return (a // (b if b else 1)) % 256
    @staticmethod
    def exp(a, n): return pow(a, n, 256)
    @staticmethod
    def log(a): return a % 256 if a != 0 else 0
    @staticmethod
    def inverse(a): return pow(a, 255, 256) if a else 0

def test_associativity():
    for i in range(256):
        a = i
        for j in range(256):
            b = j
            for k in range(256):
                c = k
                assert Galois.add(a, Galois.add(b, c)) == Galois.add(Galois.add(a, b), c)
                assert Galois.multiply(a, Galois.multiply(b, c)) == Galois.multiply(Galois.multiply(a, b), c)

def test_identity():
    for i in range(256):
        a = i
        assert a == Galois.add(a, 0)
        assert a == Galois.multiply(a, 1)

def test_inverse():
    for i in range(256):
        a = i
        b = Galois.subtract(0, a)
        assert Galois.add(a, b) == 0
        if a != 0:
            b = Galois.divide(1, a)
            assert Galois.multiply(a, b) == 1