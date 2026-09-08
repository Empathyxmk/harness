def test_public_this_behavior(capsys):
    class Obj:
        def __init__(self):
            self.value = 41
        def add(self):
            return self.value + 1

    obj = Obj()
    print(obj.add())
    captured = capsys.readouterr()
    outs = [s.strip() for s in captured.out.strip().splitlines()]
    assert outs[0] == "42"