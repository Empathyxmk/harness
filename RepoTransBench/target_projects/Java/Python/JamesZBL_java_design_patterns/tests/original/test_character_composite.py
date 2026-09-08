import io
import sys

class CharacterComposite:
    def __init__(self):
        self.children = []
    
    def add(self, child):
        self.children.append(child)

    def count(self):
        return len(self.children)

    def print(self):
        self.print_before()
        for child in self.children:
            child.print()
        self.print_after()

    def print_before(self):
        pass

    def print_after(self):
        pass

def test_add_and_count():
    composite = CharacterComposite()
    assert composite.count() == 0
    composite.add(CharacterComposite())
    assert composite.count() == 1

def test_print_no_children():
    composite = CharacterComposite()
    composite.print()  # Should not throw

def test_print_before_after_hooks():
    class TestComposite(CharacterComposite):
        def __init__(self):
            super().__init__()
            self.before_called = False
            self.after_called = False
        def print_before(self):
            self.before_called = True
        def print_after(self):
            self.after_called = True
    composite = TestComposite()
    composite.print()
    assert composite.before_called
    assert composite.after_called

def test_print_deep_composition():
    sb = []
    class MyComposite(CharacterComposite):
        def print_before(self):
            sb.append("[")
        def print_after(self):
            sb.append("]")
    class ChildComposite(CharacterComposite):
        def print_before(self):
            sb.append("A")
    composite = MyComposite()
    child = ChildComposite()
    composite.add(child)
    composite.print()
    assert "".join(sb) == "[A]"