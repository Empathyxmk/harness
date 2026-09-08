import pytest
from flask_login.mixins import UserMixin, AnonymousUserMixin

class User(UserMixin):
    def __init__(self, id):
        self.id = id

def test_user_mixin_is_active():
    user = User(1)
    assert user.is_active is True

def test_user_mixin_is_authenticated():
    user = User(2)
    assert user.is_authenticated is True

def test_user_mixin_is_anonymous():
    user = User(3)
    assert user.is_anonymous is False

def test_user_mixin_get_id_returns_str():
    user = User(123)
    assert user.get_id() == "123"
    user2 = User("abc")
    assert user2.get_id() == "abc"

def test_user_mixin_get_id_attribute_error():
    user = User(1)
    del user.id
    with pytest.raises(NotImplementedError):
        user.get_id()

def test_user_mixin_eq_true():
    user1 = User(9)
    user2 = User(9)
    assert user1 == user2

def test_user_mixin_eq_false():
    user1 = User(1)
    user2 = User(2)
    assert user1 != user2

def test_user_mixin_eq_type():
    user = User(1)
    assert (user == object()) is False  # __eq__ returns NotImplemented, which Python converts to False

def test_user_mixin_ne_type():
    user = User(1)
    assert (user != object()) is True  # __ne__ returns NotImplemented, which Python converts to True

def test_user_mixin_hash():
    user = User(1)
    assert isinstance(hash(user), int)

def test_anonymous_user_mixin_properties():
    anon = AnonymousUserMixin()
    assert anon.is_active is False
    assert anon.is_authenticated is False
    assert anon.is_anonymous is True

def test_anonymous_user_mixin_get_id():
    anon = AnonymousUserMixin()
    assert anon.get_id() is None