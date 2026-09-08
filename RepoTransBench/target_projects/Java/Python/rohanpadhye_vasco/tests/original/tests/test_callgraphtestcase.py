def test_callgraphtestcase_execution():
    # Simulate execution of CallGraphTestCase.main (class with methods foo and bar)
    called = []

    class A:
        def foo(self): self.bar()
        def bar(self): called.append("bar")

    a1 = A()
    a1.foo()
    a2 = A()
    a2.foo()
    a2.bar()

    # Test that the bar method is called the correct number of times
    # a1.foo() => a1.bar(), a2.foo() => a2.bar(), a2.bar()
    assert len(called) == 3