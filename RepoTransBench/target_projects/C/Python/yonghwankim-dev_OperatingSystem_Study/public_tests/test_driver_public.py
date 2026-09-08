# Translated from DriverPublicTest.java
import threading

# These would ~normally come from your src/ directory for implementation.
def is_prime(n):
    if n <= 1: return False
    if n == 2: return True
    if n % 2 == 0: return False
    for i in range(3, int(n**0.5)+1, 2):
        if n % i == 0: return False
    return True

def print_primes(primes, n):
    # Original just prints, so we skip actual printing here
    pass

class MyThread(threading.Thread):
    def __init__(self, name, n, primes, begin, end):
        super().__init__(name=name)
        self.n = n
        self.primes = primes
        self.begin = begin
        self.end = end
    def run(self):
        for i in range(self.begin, self.end+1):
            if is_prime(i):
                self.primes[i] = True

def test_publicSingleThreadTest():
    n = 101
    primes = [False] * (n+1)
    for i in range(1, n+1):
        if is_prime(i):
            primes[i] = True
    cnt = sum(1 for i in range(1, n+1) if primes[i])
    assert cnt == 26

def test_publicDoubleThreadTest():
    n = 200
    primes = [False] * (n+1)
    thread1 = MyThread("t1", n, primes, 1, n//2)
    thread2 = MyThread("t2", n, primes, (n//2)+1, n)
    thread1.start(); thread2.start()
    thread1.join(); thread2.join()
    cnt = sum(1 for i in range(1, n+1) if primes[i])
    assert cnt == 46

def test_publicTripleThreadTest():
    n = 500
    primes = [False] * (n+1)
    thread1 = MyThread("t1", n, primes, 1, n//3)
    thread2 = MyThread("t2", n, primes, (n//3)+1, ((n//3)+1)*2)
    thread3 = MyThread("t3", n, primes, ((n//3)+1)*2, n)
    thread1.start(); thread2.start(); thread3.start()
    thread1.join(); thread2.join(); thread3.join()
    cnt = sum(1 for i in range(1, n+1) if primes[i])
    assert cnt == 95