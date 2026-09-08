import pytest

class SimpleEntity:
    def __init__(self, id):
        self.id = id
    def getId(self):
        return self.id
    def setId(self, id):
        self.id = id

class Order:
    def __init__(self, column, asc):
        self._column = column
        self._asc = asc
    def getColumn(self):
        return self._column
    def isAsc(self):
        return self._asc

class Match:
    def __init__(self, column, value):
        self._column = column
        self._value = value
    def getColumn(self):
        return self._column
    def getValue(self):
        return self._value

class Modify:
    def __init__(self, column, value):
        self._column = column
        self._value = value
    def getColumn(self):
        return self._column
    def getValue(self):
        return self._value

class DaoPage:
    def __init__(self):
        self.page_no = 1
        self.page_size = 10
    def setPageNo(self, page_no):
        self.page_no = page_no
    def setPageSize(self, page_size):
        self.page_size = page_size

class DaoPageResult:
    def __init__(self, items, total_count):
        self._items = items
        self._total_count = total_count
    def getResult(self):
        return self._items
    def getTotalCount(self):
        return self._total_count

class AbstractDao:
    def order(self, column, asc):
        return Order(column, asc)
    def match(self, column, value):
        return Match(column, value)
    def modify(self, column, value):
        return Modify(column, value)
    def toList(self, *args):
        return list(args)
    def page2(self, match_list, page):
        # Always returns two items for mock, and total count 42
        return DaoPageResult([SimpleEntity(1), SimpleEntity(2)], 42)
    def like(self, s):
        return f"%{s}%"
    def between(self, a, b):
        return (a, b)
    def greaterThan(self, x):
        return (">", x)
    def lessThan(self, x):
        return ("<", x)
    def express(self):
        return "EXPR"
    def not_(self, v):
        return f"NOT {v}"
    def incr(self, v):
        return v + 1

class SimpleDao(AbstractDao):
    def get(self, id):
        return SimpleEntity(id)
    def find(self, matchList, orderList, offset=None, limit=None):
        return [SimpleEntity(1), SimpleEntity(2)]
    def count(self, matchList):
        return 42

def test_order_match_modify():
    dao = SimpleDao()
    order = dao.order("col", True)
    assert order.getColumn() == "col"
    assert order.isAsc()

    match = dao.match("foo", 1)
    assert match.getColumn() == "foo"
    assert match.getValue() == 1

    modify = dao.modify("bar", 2)
    assert modify.getColumn() == "bar"
    assert modify.getValue() == 2

def test_to_list():
    dao = SimpleDao()
    empty = dao.toList()
    assert len(empty) == 0
    vals = dao.toList(1, "abc", 3.4)
    assert len(vals) == 3
    assert vals[1] == "abc"

def test_page2():
    dao = SimpleDao()
    page = DaoPage()
    page.setPageNo(1)
    page.setPageSize(20)
    result = dao.page2([dao.match("foo", 123)], page)
    assert result.getResult() is not None
    assert result.getTotalCount() == 42

def test_like_between_greater_less_express_not_incr():
    dao = SimpleDao()
    assert dao.like("str") is not None
    assert dao.between(1, 5) == (1, 5)
    assert dao.greaterThan(9) == (">", 9)
    assert dao.lessThan(5) == ("<", 5)
    assert dao.express() == "EXPR"
    assert dao.not_("notVal") == "NOT notVal"
    assert dao.incr(3) == 4