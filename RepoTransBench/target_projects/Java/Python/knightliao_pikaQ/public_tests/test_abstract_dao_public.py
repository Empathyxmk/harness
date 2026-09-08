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
        # Always returns two items (different IDs for public test), total count 77
        return DaoPageResult([SimpleEntity(3), SimpleEntity(4)], 77)
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
        return [SimpleEntity(3), SimpleEntity(4)]
    def count(self, matchList):
        return 77

def test_order_match_modify():
    dao = SimpleDao()
    order = dao.order("otherCol", False)
    assert order.getColumn() == "otherCol"
    assert not order.isAsc()

    match = dao.match("bar", 5)
    assert match.getColumn() == "bar"
    assert match.getValue() == 5

    modify = dao.modify("baz", 8)
    assert modify.getColumn() == "baz"
    assert modify.getValue() == 8

def test_to_list():
    dao = SimpleDao()
    empty = dao.toList()
    assert len(empty) == 0
    vals = dao.toList("test", 42, 7.8, False)
    assert len(vals) == 4
    assert vals[1] == 42
    assert vals[3] is False

def test_page2():
    dao = SimpleDao()
    page = DaoPage()
    page.setPageNo(2)
    page.setPageSize(10)
    result = dao.page2([dao.match("bar", 456)], page)
    assert result.getResult() is not None
    assert result.getTotalCount() == 77

def test_like_between_greater_less_express_not_incr():
    dao = SimpleDao()
    assert dao.like("otherStr") is not None
    assert dao.between(2, 8) == (2, 8)
    assert dao.greaterThan(15) == (">", 15)
    assert dao.lessThan(1) == ("<", 1)
    assert dao.express() == "EXPR"
    assert dao.not_("anotherVal") == "NOT anotherVal"
    assert dao.incr(10) == 11