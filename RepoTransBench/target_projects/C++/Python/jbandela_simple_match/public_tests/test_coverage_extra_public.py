import pytest
import re

def test_regex_public(capsys):
    # Support area codes
    area_codes = {"312", "305", "404", "212", "617"}

    def support(s):
        return s in area_codes

    r_cfg = re.compile(r"([A-Z]+)\.cfg")
    def m(s):
        out = []
        mobj = r_cfg.search(s)
        if mobj:
            print(mobj.group(1))
            return
        mobj2 = re.search(r"([0-9]{2,4})/([0-9]{2})/([0-9]{2})", s)
        if mobj2:
            y, m, d = int(mobj2.group(1)), int(mobj2.group(2)), int(mobj2.group(3))
            print(f"Parsed: {y}/{m}/{d}")
            return
        m_phone = re.match(r"([0-9]{3})-([0-9]+)-([0-9]+)", s)
        if m_phone:
            code, y, z = m_phone.group(1), m_phone.group(2), m_phone.group(3)
            if code == "305":
                print(f"Miami local {y}-{z}")
                return
            elif code in area_codes:
                print(f"Support code {code}-{y}-{z}")
                return
            else:
                print(f"Other phone {code}-{y}-{z}")
                return
        print(f"{s} No regex match")

    m("CONFIG.CFG")
    m("2022/12/31")
    m("202/02/25")
    m("299/11/12")
    m("305-555-1212")
    m("404-999-8888")
    m("650-111-2222")

def test_variant_public():
    class Sum:
        def __init__(self, a, b):
            self.a = a
            self.b = b
    class Diff:
        def __init__(self, a, b):
            self.a = a
            self.b = b
    class Prod:
        def __init__(self, a, b):
            self.a = a
            self.b = b
    class Inv:
        def __init__(self, x):
            self.x = x

    def eval_public(e):
        # Fused add-mul
        if isinstance(e, Sum) and isinstance(e.b, Prod) \
            and isinstance(e.a, int) and isinstance(e.b.a, int) and isinstance(e.b.b, int):
            x = e.a
            y = e.b.a
            z = e.b.b
            print(f"Fused sum-product: {x}+{y}*{z}")
            return x + y * z
        # Simple sum
        elif isinstance(e, Sum) and isinstance(e.a, int) and isinstance(e.b, int):
            x, y = e.a, e.b
            print(f"Simple sum {x}+{y}")
            return x + y
        elif isinstance(e, Prod) and isinstance(e.a, int) and isinstance(e.b, int):
            x, y = e.a, e.b
            print(f"Product {x}*{y}")
            return x * y
        elif isinstance(e, Diff) and isinstance(e.a, int) and isinstance(e.b, int):
            x, y = e.a, e.b
            print(f"Difference {x}-{y}")
            return x - y
        elif isinstance(e, Inv) and isinstance(e.x, int):
            x = e.x
            print(f"Inverse -{x}")
            return -x
        elif isinstance(e, int):
            print(f"Just value {e}")
            return e
        else:
            raise ValueError("Unsupported type for eval_public")

    s = Sum(2, Prod(3, 4))
    d = Diff(9, 5)
    p = Prod(6, 7)
    n = Inv(8)
    simple_sum = Sum(12, 30)
    value = 44

    x = eval_public(s) # 2 + 3*4 == 14
    y = eval_public(d) # 9-5 == 4
    z = eval_public(p) # 6*7 == 42
    w = eval_public(n) # -8
    sum_simple = eval_public(simple_sum) # 42
    val_only = eval_public(value) # 44

    assert x == 14
    assert y == 4
    assert z == 42
    assert w == -8
    assert sum_simple == 42
    assert val_only == 44