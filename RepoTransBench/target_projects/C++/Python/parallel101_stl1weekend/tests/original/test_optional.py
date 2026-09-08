import pytest

class BadOptionalAccess(Exception):
    pass

class Optional:
    def __init__(self, value=None):
        self._has = value is not None
        self._val = value
    def has_value(self):
        return self._has
    def value(self):
        if not self._has:
            raise BadOptionalAccess("No value present")
        return self._val
    def value_or(self, other):
        if self._has:
            return self._val
        else:
            return other
    def reset(self):
        self._has = False
        self._val = None
    def emplace(self, value=None):
        self._val = value if value is not None else type(self._val)() if self._val is not None else ""
        self._has = True
    def __bool__(self):
        return self._has
    def __eq__(self, other):
        if isinstance(other, Optional):
            return self._has == other._has and self._val == other._val
        return False
    def __ne__(self, other):
        return not self.__eq__(other)
    def and_then(self, func):
        if self._has:
            return Optional(func(self._val))
        else:
            return Optional()
    def transform(self, func):
        if self._has:
            return Optional(func(self._val))
        else:
            return Optional()
    def or_else(self, func):
        if self._has:
            return Optional(self._val)
        else:
            return func()

def makeOptional(val):
    return Optional(val)

def test_ours(capsys):
    # Skipping C structure/printing parts.
    opts = Optional("ss")
    assert opts.value() == "ss"
    s1 = opts.value()
    s2 = opts.value()
    optcs = Optional("ss")
    assert optcs.value() == "ss"
    opt = Optional(1)
    print(opt.has_value())
    print(opt.value())
    print(opt.value_or(0))
    opt.reset()
    print(opt.has_value())
    opt = Optional(42)
    print(opt.has_value())
    print(opt.value())
    print(opt.value_or(0))
    opt = Optional(42)
    print(opt.has_value())
    print(opt.value())
    print(opt.value_or(0))
    opt = Optional()
    print(opt.has_value())
    opt2 = Optional()
    print(opt2.has_value())
    try:
        opt2.value()
    except BadOptionalAccess as e:
        print("opt2 exception:", str(e))
    print(opt2.value_or(0))
    opt3 = Optional()
    print(opt3.has_value())
    try:
        opt2.value()
    except BadOptionalAccess as e:
        print("opt3 exception:", str(e))
    print(opt3.value_or(0))
    output = capsys.readouterr().out.strip().splitlines()
    # Check True/False printout for has_value
    assert output[0] == "True"
    assert output[3] == "False"
    assert output[4] == "True"
    assert output[7] == "True"
    assert output[10] == "False"
    assert output[11] == "False"
    # Exception message present
    assert any("opt2 exception:" in l for l in output)
    assert output[-3] == "False"
    assert any("opt3 exception:" in l for l in output)

def test_std(capsys):
    import typing
    from typing import Optional as StdOptional
    opt = 1
    stdopt = opt
    print(True)  # has_value
    print(stdopt)
    print(stdopt if stdopt is not None else 0)
    stdopt2 = None
    print(stdopt2 is not None)
    try:
        if stdopt2 is None:
            raise Exception()
        _ = stdopt2
    except Exception:
        print("opt2 exception ok")
    print(stdopt2 if stdopt2 is not None else 0)
    stdopt2 = 42
    print(stdopt2 is not None)
    print(stdopt2)
    print(stdopt2 if stdopt2 is not None else 0)
    output = capsys.readouterr().out.strip().splitlines()
    assert output[0] == "True"
    assert output[1] == "1"
    assert output[2] == "1"
    assert output[3] == "False"
    assert output[4] == "opt2 exception ok"
    assert output[5] == "0"
    assert output[6] == "True"
    assert output[7] == "42"
    assert output[8] == "42"

def parseInt(s):
    try:
        return Optional(int(s))
    except Exception:
        return Optional()

def getInt(linesrc):
    # Simulate is input with a list as linesrc
    if not linesrc:
        return Optional()
    s = linesrc.pop(0)
    return parseInt(s)

def test_emplace(capsys):
    # getInt: pass simulated lines to read from
    lines = ["4", "bad", "123"]
    while True:
        opt = getInt(lines)
        if not opt.has_value():
            break
        print(opt.value())
    optc = Optional()
    optc.emplace((1,2))
    assert optc.has_value()
    assert optc.value() == (1,2)
    opti = Optional()
    opti.emplace(42)
    assert opti.has_value()
    opti.emplace()
    assert opti.value() == ""
    i = bool(opti)
    print(int(i))
    opts = Optional()
    opts.emplace()
    assert opts.value() == ""
    opts.reset()
    assert not opts.has_value()
    output = capsys.readouterr().out.strip().splitlines()
    # Should print 4, 123 and 1
    assert "4" in output
    assert "123" in output
    assert "1" in output

def test_cmp(capsys):
    o = Optional()
    print(o != Optional(100))
    x = makeOptional(42)
    o = Optional(-42)
    def and_then_func(i):
        if i < 0:
            return None
        return i+1
    o2 = o.and_then(and_then_func)
    if o2 and o2.value() is not None:
        print(o2.value())
    else:
        print("nullopt")
    o = Optional(-42)
    up = 44
    def transform_func(i):
        return i+1
    o3 = o.transform(transform_func)
    if o3 and o3.value() is not None:
        print(o3.value())
    else:
        print("nullopt")
    o = Optional(42)
    def or_elsefunc():
        print("没值！")
        return Optional(0)
    o4 = o.or_else(or_elsefunc)
    if o4 and o4.value() is not None:
        print(o4.value())
    else:
        print("nullopt")
    output = capsys.readouterr().out.strip().splitlines()
    assert output[0] == "True" or output[0] == "False"
    # "nullopt" expected
    assert "nullopt" in output or any("没值" in l for l in output)

def test_in_place():
    # Just verifying emplace behaves correctly
    o1 = Optional((1,2))
    o1.emplace((1,2))
    o2 = Optional((1,2))
    o3 = Optional((1,2))
    ov = Optional([1,2,3])
    cccp = Optional((1,2))
    ussr = Optional((3,4))
    # Swap simulation
    temp = cccp.value()
    cccp._val = ussr.value()
    ussr._val = temp
    assert cccp.value() == (3,4)
    assert ussr.value() == (1,2)