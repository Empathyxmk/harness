import pickle
import json
from qcore.enum import Enum, Flags, IntEnum
from qcore.asserts import (
    assert_eq,
    assert_is,
    assert_ne,
    assert_raises,
    assert_in,
    assert_not_in,
    assert_is_instance,
)

class Status(Enum):
    unknown = 0
    active = 10
    closed = 20

    @property
    def inverted(self):
        assert self.is_valid()
        if self.value == 0:
            return Status.unknown
        return Status(30 - self.value)

class OtherEnum(IntEnum):
    none = 0
    up = 10
    down = 20

def _public_assert_equality_both_directions(left, right, not_equal):
    assert_eq(left, right)
    assert_eq(right, left)
    assert_ne(not_equal, right)
    assert_ne(right, not_equal)

def test_public_status():
    assert_eq([20, 10], Status._flag_values)
    assert_eq([Status.unknown, Status.active, Status.closed], Status.get_members())
    assert_eq(["unknown", "active", "closed"], Status.get_names())
    assert_eq(3, len(Status))

    _public_assert_equality_both_directions(0, Status.unknown, 1)
    _public_assert_equality_both_directions(10, Status.active, 20)
    _public_assert_equality_both_directions(20, Status.closed, 30)

    _public_assert_equality_both_directions(
        Status.unknown, Status.parse("unknown"), Status.active
    )
    _public_assert_equality_both_directions(Status.active, Status.parse("active"), Status.closed)
    _public_assert_equality_both_directions(Status.closed, Status.parse("closed"), Status.active)

    _public_assert_equality_both_directions(
        Status.unknown, Status.parse(Status.unknown), Status.active
    )
    _public_assert_equality_both_directions(
        Status.active, Status.parse(Status.active), Status.closed
    )
    _public_assert_equality_both_directions(
        Status.closed, Status.parse(Status.closed), Status.active
    )

    assert_is(None, Status.parse("n/a", None))
    assert_raises(lambda: Status.parse("n/a"), KeyError)
    assert_raises(lambda: Status.parse(OtherEnum.none), KeyError)
    assert_raises(lambda: Status.parse(b"random"), KeyError)
    assert_raises(lambda: Status.parse("random"), KeyError)
    assert_raises(lambda: Status.parse(b"foo\xff"), KeyError)
    assert_raises(lambda: Status.parse("\u03b1\u03b2\u03b3"), KeyError)

    assert_eq("unknown", Status(0).short_name)
    assert_eq("active", Status(10).short_name)
    assert_eq("closed", Status(20).short_name)

    assert_eq("Status.closed", Status.closed.long_name)
    assert_eq("Closed", Status.closed.title)
    assert_eq("test_public_enum.Status.closed", Status.closed.full_name)

    assert_is(None, Status.parse("", None))
    assert_is(None, Status.parse(99, None))
    assert_raises(lambda: Status.parse(""), KeyError)
    assert_raises(lambda: Status.parse(99), KeyError)
    assert_is(None, Status("", None))
    assert_is(None, Status(99, None))
    assert_raises(lambda: Status(""), KeyError)
    assert_raises(lambda: Status(99), KeyError)

    assert_eq(str(Status.active), "active")
    assert_eq(repr(Status.active), "Status.active")

def test_public_inverted_property():
    assert_eq(Status.unknown.inverted, Status.unknown)
    assert_eq(Status.active.inverted, Status.closed)
    assert_eq(Status.closed.inverted, Status.active)

def test_public_enum_create():
    def helper(cls):
        assert_eq([cls.active, cls.closed], cls.get_members())
        assert_eq([cls.active, cls.closed], list(cls))
        assert_eq(10, cls.active)
        assert_eq(20, cls.closed)
        assert_eq(cls.active, Status.active)
        assert_eq(cls.closed, Status.closed)
        assert_in(cls.active, cls)

        assert_eq(cls.active, cls.parse(10))
        assert_eq(cls.active, cls.parse("active"))
        assert_eq(cls.active, cls.parse(cls.active))
        assert_eq(cls.active, cls(10))
        assert_eq(cls.active, cls("active"))
        assert_eq(cls.active, cls(cls.active))

    class OnlyActiveClosed(Enum):
        active = Status.active
        closed = Status.closed

    helper(OnlyActiveClosed)

    cls2 = Enum.create("OnlyActiveClosed", [Status.active, Status.closed])
    helper(cls2)

    cls3 = Enum.create("OnlyActiveClosed", {"active": 10, "closed": 20})
    helper(cls3)

    cls4 = Enum.create("OnlyActiveClosed", [("active", 10), ("closed", 20)])
    helper(cls4)

class AbcFlag(Flags):
    a = 1
    b = 2
    c = 4
    ab = 3

class DefAbc(AbcFlag):
    d = 8
    e = 16
    f = 32
    abc = 7

class AllStatus(DefAbc):
    none = 0

def test_public_flags():
    assert_eq([32, 16, 8, 7, 4, 3, 2, 1], DefAbc._flag_values)
    assert_eq([AbcFlag.a, AbcFlag.b, AbcFlag.c, AbcFlag.ab], AbcFlag.get_members())
    assert_eq([DefAbc.a, DefAbc.b, DefAbc.c, DefAbc.ab, DefAbc.d, DefAbc.e, DefAbc.f, DefAbc.abc], DefAbc.get_members())
    assert_eq(
        [AllStatus.none, AllStatus.a, AllStatus.b, AllStatus.c, AllStatus.ab, AllStatus.d, AllStatus.e, AllStatus.f, AllStatus.abc],
        AllStatus.get_members(),
    )
    assert_eq(
        str(AllStatus.get_members()),
        "[AllStatus.none, AllStatus.a, AllStatus.b, AllStatus.c, AllStatus.ab, AllStatus.d, AllStatus.e, AllStatus.f, AllStatus.abc]",
    )

    assert_eq(0, DefAbc.parse(""))
    assert_eq(0, DefAbc.parse(0))
    assert_eq(0, AllStatus.parse("none"))
    assert_is(None, DefAbc.parse("none", None))
    assert_eq(0, DefAbc(""))
    assert_eq(0, DefAbc(0))
    assert_eq(0, AllStatus("none"))
    assert_is(None, DefAbc("none", None))

    assert_raises(lambda: DefAbc.parse("_"), KeyError)

    # Pickle
    for v in [DefAbc.d, DefAbc.e]:
        pickled = pickle.dumps(v)
        assert_eq(pickle.loads(pickled), v)

    # JSON encoding
    assert_eq(json.loads(json.dumps(DefAbc.c)), 4)
    assert_eq(json.loads(json.dumps(DefAbc.f)), 32)