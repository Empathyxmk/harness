import pytest
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))

from randexp.randexp import RandExp

def test_randexp_generate_valid_emails():
    re_ = RandExp(r"\w{4,9}@test\.org")
    for _ in range(10):
        s = re_.gen()
        assert RandExp(r"^[A-Za-z0-9_]{4,9}@test\.org$").match(s)

def test_randexp_handle_groups_and_quantifiers():
    re_ = RandExp(r"(hi|bye){3}")
    for _ in range(5):
        s = re_.gen()
        assert RandExp(r"^(hi|bye){3}$").match(s)

def test_randexp_handle_optional_groups():
    re_ = RandExp(r"^ok(yes)?$")
    for _ in range(8):
        s = re_.gen()
        assert RandExp(r"^ok(yes)?$").match(s)

def test_randexp_support_capture_groups():
    re_ = RandExp(r"(foo)(bar)?")
    for _ in range(8):
        s = re_.gen()
        assert RandExp(r"^(foo)(bar)?$").match(s)