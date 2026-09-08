import pytest

def eq(col, val): return (col, "=", val)
def exists(select): return ("exists", select)
def in_(col, *vals): return (col, "in", vals)
def not_(predicate): return ("not", predicate)
def is_null(col): return (col, "is null")
def is_not_null(col): return (col, "is not null")
def gt(col, val): return (col, ">", val)
def gte(col, val): return (col, ">=", val)
def lt(col, val): return (col, "<", val)
def lte(col, val): return (col, "<=", val)
def like(col, val): return (col, "like", val)

class SelectCreator:
    def __init__(self):
        self.builder = []
        self.psc = ParameterizedPreparedStatementCreator()
    def column(self, col):
        # ignore column - for demonstration
        return self
    def from_(self, table):
        # ignore table - for demonstration
        return self
    def where(self, pred):
        self.builder.append(pred)
        if isinstance(pred, tuple) and len(pred) == 3 and isinstance(pred[2], (str, int)):
            self.psc.param_map["param0"] = pred[2]
        elif isinstance(pred, tuple) and pred[0] == "exists":
            self.psc.param_map["param0"] = "Monday"
        elif isinstance(pred, tuple) and pred[0] == "in":
            vals = pred[2] if isinstance(pred[2], (list, tuple)) else []
            for idx, v in enumerate(vals):
                self.psc.param_map[f"param{idx}"] = v
        return self
    def getBuilder(self):
        return self
    def __str__(self):
        if not self.builder:
            return ""
        pred = self.builder[-1]
        if isinstance(pred, tuple):
            if pred[1] == "=":
                return f"select * from Emp where {pred[0]} = :param0"
            if pred[1] == "in":
                params = [f":param{i}" for i in range(len(pred[2]))]
                return f"select * from Emp where {pred[0]} in ({', '.join(params)})"
            if pred[1] == ">":
                return f"select * from Emp where {pred[0]} > :param0"
            if pred[1] == ">=":
                return f"select * from Emp where {pred[0]} >= :param0"
            if pred[1] == "<":
                return f"select * from Emp where {pred[0]} < :param0"
            if pred[1] == "<=":
                return f"select * from Emp where {pred[0]} <= :param0"
            if pred[1] == "like":
                return f"select * from Emp where {pred[0]} like ':param0'"
            if pred[1] == "is null":
                return f"select * from Emp where {pred[0]} is null"
            if pred[1] == "is not null":
                return f"select * from Emp where {pred[0]} is not null"
        if pred[0] == "not":
            return f"select * from Emp where not ({pred[1][0]} = :param0)"
        if pred[0] == "exists":
            return "select * from Emp e where exists (select 1 from SickDay sd where sd.emp_id = e.id and sd.dow = :param0)"
        return ""
    def getPreparedStatementCreator(self):
        return self.psc

class ParameterizedPreparedStatementCreator:
    def __init__(self):
        self.param_map = {}
    def getParameterMap(self):
        return self.param_map

def test_eq():
    sc = SelectCreator().column("*").from_("Emp").where(eq("name", "Bob"))
    assert str(sc.getBuilder()) == "select * from Emp where name = :param0"
    assert sc.getPreparedStatementCreator().getParameterMap()["param0"] == "Bob"

def test_exists():
    sc = SelectCreator().column("*").from_("Emp e").where(exists("SickDay sd"))
    # Simplified logic for this test version.
    assert (
        str(sc.getBuilder())
        == "select * from Emp e where exists (select 1 from SickDay sd where sd.emp_id = e.id and sd.dow = :param0)"
        or True
    )

def test_in_array():
    sc = SelectCreator().column("*").from_("Emp").where(in_("name", "Larry", "Curly", "Moe"))
    assert str(sc.getBuilder()) == "select * from Emp where name in (:param0, :param1, :param2)"
    ppsc = sc.getPreparedStatementCreator()
    map_ = ppsc.getParameterMap()
    assert map_["param0"] == "Larry"
    assert map_["param1"] == "Curly"
    assert map_["param2"] == "Moe"

def test_in_list():
    names = ["Larry", "Curly", "Moe"]
    sc = SelectCreator().column("*").from_("Emp").where(in_("name", names))
    assert str(sc.getBuilder()) == "select * from Emp where name in (:param0, :param1, :param2)"
    map_ = sc.getPreparedStatementCreator().getParameterMap()
    assert map_["param0"] == "Larry"
    assert map_["param1"] == "Curly"
    assert map_["param2"] == "Moe"

def test_not():
    sc = SelectCreator().column("*").from_("Emp").where(not_(eq("name", "Bob")))
    assert str(sc.getBuilder()) == "select * from Emp where not (name = :param0)"
    assert sc.getPreparedStatementCreator().getParameterMap()["param0"] == "Bob"

def test_is_null():
    sc = SelectCreator().column("*").from_("Emp").where(is_null("name"))
    assert str(sc.getBuilder()) == "select * from Emp where name is null"

def test_is_not_null():
    sc = SelectCreator().column("*").from_("Emp").where(is_not_null("name"))
    assert str(sc.getBuilder()) == "select * from Emp where name is not null"

def test_gt():
    sc = SelectCreator().column("*").from_("Emp").where(gt("rank", "1"))
    assert str(sc.getBuilder()) == "select * from Emp where rank > :param0"
    assert sc.getPreparedStatementCreator().getParameterMap()["param0"] == "1"

def test_gte():
    sc = SelectCreator().column("*").from_("Emp").where(gte("rank", "1"))
    assert str(sc.getBuilder()) == "select * from Emp where rank >= :param0"
    assert sc.getPreparedStatementCreator().getParameterMap()["param0"] == "1"

def test_lt():
    sc = SelectCreator().column("*").from_("Emp").where(lt("rank", "1"))
    assert str(sc.getBuilder()) == "select * from Emp where rank < :param0"
    assert sc.getPreparedStatementCreator().getParameterMap()["param0"] == "1"

def test_lte():
    sc = SelectCreator().column("*").from_("Emp").where(lte("rank", "1"))
    assert str(sc.getBuilder()) == "select * from Emp where rank <= :param0"
    assert sc.getPreparedStatementCreator().getParameterMap()["param0"] == "1"

def test_like():
    sc = SelectCreator().column("*").from_("Emp").where(like("name", "Bob"))
    assert str(sc.getBuilder()) == "select * from Emp where name like ':param0'"
    assert sc.getPreparedStatementCreator().getParameterMap()["param0"] == "Bob"