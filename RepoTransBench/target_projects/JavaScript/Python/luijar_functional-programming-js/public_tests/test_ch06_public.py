def compose(f, g):
    return lambda x: f(g(x))

def test_public_compose_upper_and_exclaim():
    upper = lambda x: x.upper()
    exclaim = lambda x: x + "!"
    loud = compose(exclaim, upper)
    assert loud("hey") == "HEY!"

def test_public_map_negative():
    xs = [1,2,3]
    f = lambda x: -x
    assert list(map(f, xs)) == [-1,-2,-3]