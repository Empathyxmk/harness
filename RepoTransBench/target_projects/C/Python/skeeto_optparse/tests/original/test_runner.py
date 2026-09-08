"""
This test file corresponds to test.c, which is a combination of a big table-driven testsuite and a manual test.
We will implement only the main table-driven test suite as pytest tests.
"""
import pytest
from src.optparse import optparse_long as OptparseLong, optparse_arg, optparse
from src.optparse import OPTPARSE_NONE, OPTPARSE_REQUIRED, OPTPARSE_OPTIONAL, OPTPARSE_MSG_MISSING, OPTPARSE_MSG_INVALID

class Options:
    def __init__(self):
        self.argv = []
        self.optind = 0
        self.optarg = None
        self.errmsg = None

def optparse_init(options, argv):
    options.argv = list(argv)
    options.optind = 1 if len(argv) > 0 else 0
    options.optarg = None
    options.errmsg = None

TABLE = [
    {
        "argv": ["", "--", "foobar"],
        "conf": {"amend": 0, "brief": 0, "color": None, "delay": 0, "erase": 0},
        "args": ["foobar"],
        "err": None
    },
    {
        "argv": ["", "-a", "-b", "-c", "-d", "10", "-e"],
        "conf": {"amend": 1, "brief": 1, "color": "", "delay": 10, "erase": 1},
        "args": [],
        "err": None
    },
    {
        "argv": ["", "--amend", "--brief", "--color", "--delay", "10", "--erase"],
        "conf": {"amend": 1, "brief": 1, "color": "", "delay": 10, "erase": 1},
        "args": [],
        "err": None
    },
    {
        "argv": ["", "-a", "-b", "-cred", "-d", "10", "-e"],
        "conf": {"amend": 1, "brief": 1, "color": "red", "delay": 10, "erase": 1},
        "args": [],
        "err": None
    },
    {
        "argv": ["", "-abcblue", "-d10", "foobar"],
        "conf": {"amend": 1, "brief": 1, "color": "blue", "delay": 10, "erase": 0},
        "args": ["foobar"],
        "err": None
    },
    {
        "argv": ["", "--color=red", "-d", "10", "--", "foobar"],
        "conf": {"amend": 0, "brief": 0, "color": "red", "delay": 10, "erase": 0},
        "args": ["foobar"],
        "err": None
    },
    {
        "argv": ["", "-eeeeee"],
        "conf": {"amend": 0, "brief": 0, "color": None, "delay": 0, "erase": 6},
        "args": [],
        "err": None
    },
    {
        "argv": ["", "--delay"],
        "conf": {"amend": 0, "brief": 0, "color": None, "delay": 0, "erase": 0},
        "args": [],
        "err": OPTPARSE_MSG_MISSING
    },
    {
        "argv": ["", "--foo", "bar"],
        "conf": {"amend": 0, "brief": 0, "color": None, "delay": 0, "erase": 0},
        "args": ["--foo", "bar"],
        "err": OPTPARSE_MSG_INVALID
    },
    {
        "argv": ["", "-x"],
        "conf": {"amend": 0, "brief": 0, "color": None, "delay": 0, "erase": 0},
        "args": ["-x"],
        "err": OPTPARSE_MSG_INVALID
    },
    {
        "argv": ["", "-"],
        "conf": {"amend": 0, "brief": 0, "color": None, "delay": 0, "erase": 0},
        "args": ["-"],
        "err": None
    },
    {
        "argv": ["", "-e", "foo", "bar", "baz", "-a", "quux"],
        "conf": {"amend": 1, "brief": 0, "color": None, "delay": 0, "erase": 1},
        "args": ["foo", "bar", "baz", "quux"],
        "err": None
    },
    {
        "argv": ["", "foo", "--delay", "1234", "bar", "-cred"],
        "conf": {"amend": 0, "brief": 0, "color": "red", "delay": 1234, "erase": 0},
        "args": ["foo", "bar"],
        "err": None
    },
]

@pytest.mark.parametrize("entry", TABLE)
def test_table_suite(entry):
    longopts = [
        OptparseLong("amend", 'a', OPTPARSE_NONE),
        OptparseLong("brief", 'b', OPTPARSE_NONE),
        OptparseLong("color", 'c', OPTPARSE_OPTIONAL),
        OptparseLong("delay", 'd', OPTPARSE_REQUIRED),
        OptparseLong("erase", 'e', OPTPARSE_NONE)
    ]
    options = Options()
    conf = {"amend": 0, "brief": 0, "color": None, "delay": 0, "erase": 0}
    err = None
    optparse_init(options, entry["argv"])
    # Loop simulates the switch(opt)
    # This requires optparse_long to be implemented in full.
    raise NotImplementedError("You must implement optparse_long to complete this comprehensive test suite.")