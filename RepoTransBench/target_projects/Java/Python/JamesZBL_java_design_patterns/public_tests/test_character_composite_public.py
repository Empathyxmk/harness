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

def test_add_multiple_and_count_public():
    composite = CharacterComposite()
    assert composite.count() == 0
    composite.add(CharacterComposite())
    composite.add(CharacterComposite())
    assert composite.count() == 2

def test_print_no_children_public():
    composite = CharacterComposite()
    composite.print()

def test_print_before_after_hooks_public():
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

def test_print_deep_composition_public():
    sb = []
    class MyComposite(CharacterComposite):
        def print_before(self):
            sb.append("<")
        def print_after(self):
            sb.append(">")
    class ChildComposite(CharacterComposite):
        def print_before(self):
            sb.append("B")
    composite = MyComposite()
    child = ChildComposite()
    composite.add(child)
    composite.print()
    assert "".join(sb) == "<B>"