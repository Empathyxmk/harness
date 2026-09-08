import pytest

class PublicSample:
    pass

class PublicSampleHolder:
    sample = None

class ReifiedParameterizedType:
    def __init__(self, param_type):
        self.pt = param_type
        self._args = []
        self._max_args = 2

    def addReifiedTypeArgument(self, typ):
        if len(self._args) < self._max_args:
            self._args.append(typ)

    def getActualTypeArguments(self):
        return self._args

    def __str__(self):
        result = []
        for arg in self._args:
            if arg is self:
                result.append("...")
            elif arg is None:
                result.append("null")
            elif hasattr(arg, "__name__"):
                result.append(arg.__name__)
            else:
                result.append(str(arg))
        return f"{self.pt}[{', '.join(result)}]"

    def __eq__(self, other):
        if not isinstance(other, ReifiedParameterizedType):
            return False
        return self.pt == other.pt and self._args == other._args

    def __hash__(self):
        return hash((self.pt, tuple(self._args)))


def get_parameterized_type():
    return PublicSampleHolder

def test_add_reified_type_argument_normal():
    pt = get_parameterized_type()
    rpt = ReifiedParameterizedType(pt)
    rpt.addReifiedTypeArgument(float)
    rpt.addReifiedTypeArgument(str)
    assert rpt.getActualTypeArguments()[0] == float
    assert rpt.getActualTypeArguments()[1] == str

def test_add_reified_type_argument_loop():
    pt = get_parameterized_type()
    rpt = ReifiedParameterizedType(pt)
    rpt.addReifiedTypeArgument(rpt)
    rpt.addReifiedTypeArgument(str)
    assert rpt.getActualTypeArguments()[0] is rpt
    assert rpt.getActualTypeArguments()[1] == str
    s = str(rpt)
    assert "..." in s

def test_add_reified_type_argument_overflow():
    pt = get_parameterized_type()
    rpt = ReifiedParameterizedType(pt)
    rpt.addReifiedTypeArgument(float)
    rpt.addReifiedTypeArgument(str)
    rpt.addReifiedTypeArgument(bool)
    args = rpt.getActualTypeArguments()
    assert len(args) == 2

def test_to_string_owner_type():
    pt = get_parameterized_type()
    rpt = ReifiedParameterizedType(pt)
    rpt.addReifiedTypeArgument(None)
    rpt.addReifiedTypeArgument(str)
    s = str(rpt)
    assert "null" in s
    assert "str" in s

def test_equals():
    pt = get_parameterized_type()
    rpt1 = ReifiedParameterizedType(pt)
    rpt2 = ReifiedParameterizedType(pt)
    rpt1.addReifiedTypeArgument(float)
    rpt1.addReifiedTypeArgument(str)
    rpt2.addReifiedTypeArgument(float)
    rpt2.addReifiedTypeArgument(str)
    assert rpt1 == rpt2
    assert rpt2 == rpt1
    rpt3 = ReifiedParameterizedType(pt)
    rpt3.addReifiedTypeArgument(str)
    rpt3.addReifiedTypeArgument(float)
    assert rpt1 != rpt3

def test_hash_code():
    pt = get_parameterized_type()
    rpt1 = ReifiedParameterizedType(pt)
    rpt2 = ReifiedParameterizedType(pt)
    rpt1.addReifiedTypeArgument(float)
    rpt1.addReifiedTypeArgument(str)
    rpt2.addReifiedTypeArgument(float)
    rpt2.addReifiedTypeArgument(str)
    assert hash(rpt1) == hash(rpt2)

def test_not_equals_different_type():
    pt = get_parameterized_type()
    rpt = ReifiedParameterizedType(pt)
    assert rpt != "public"
    assert rpt != None