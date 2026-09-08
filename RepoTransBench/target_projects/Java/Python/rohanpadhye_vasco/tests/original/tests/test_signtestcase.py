def test_signtestcase_behavior():
    # Simulate the behavior of SignTestCase.main
    output = {}

    def five():
        return 5

    def f(a, b):
        if a < b:
            c = a * b
        else:
            c = g(10)
        return c

    def g(u):
        v = f(-u, u)
        return v

    # main
    p = five()
    q = f(p, -3)
    r = g(-q)
    output['P'] = p
    output['Q'] = q
    output['R'] = r

    # Let's add assertions to match expected flow.
    # p = 5
    # q = f(5, -3): 5 < -3 ? False --> c = g(10)
    #                g(10): v = f(-10, 10)
    #                              -10 < 10? True -> c=-10*10=-100
    #                return -100
    #            q=-100
    # r = g(-(-100)) = g(100)
    #   g(100): v = f(-100, 100)
    #             -100 < 100: True => c=-10000
    #   so r = -10000
    assert output['P'] == 5
    assert output['Q'] == -100
    assert output['R'] == -10000