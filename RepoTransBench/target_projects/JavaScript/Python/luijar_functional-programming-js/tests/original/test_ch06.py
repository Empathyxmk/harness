# Typical functional composition and functor tests
def compose(f, g):
    return lambda x: f(g(x))

def test_compose_increment_and_double():
    inc = lambda x: x+1
    dbl = lambda x: x*2
    c = compose(dbl, inc)
    assert c(3) == 8

def test_compose_double_and_increment():
    inc = lambda x: x+1
    dbl = lambda x: x*2
    c = compose(inc, dbl)
    assert c(3) == 7

def test_map_over_list():
    f = lambda x: x**2
    xs = [1,2,3]
    assert list(map(f, xs)) == [1,4,9]