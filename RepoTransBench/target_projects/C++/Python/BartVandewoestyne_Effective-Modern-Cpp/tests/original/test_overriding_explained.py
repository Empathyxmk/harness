import io
import sys

# Original C++ test rerouted main to main_overriding_explained_demo, capturing output

class Base:
    def doWork(self):
        print("Base::doWork()")

class Derived(Base):
    def doWork(self):
        print("Derived::doWork()")

def main_overriding_explained_demo():
    d = Derived()
    b = d  # In C++: Base* b = &d;
    b.doWork()

def test_prints_derived_do_work(capsys):
    main_overriding_explained_demo()
    captured = capsys.readouterr()
    assert "Derived::doWork()" in captured.out