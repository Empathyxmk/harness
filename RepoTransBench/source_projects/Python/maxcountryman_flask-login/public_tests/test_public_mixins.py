import pytest
from flask_login.mixins import UserMixin, AnonymousUserMixin

class User(UserMixin):
    def __init__(self, id):
        self.id = id

def test_user_mixin_is_active_public():
    user = User(100)
    assert user.is_active is True

def test_user_mixin_is_authenticated_public():
    user = User(200)
    assert user.is_authenticated is True

def test_user_mixin_is_anonymous_public():
    user = User(300)
    assert user.is_anonymous is False

def test_user_mixin_get_id_returns_str_public():
    user = User(456)
    assert user.get_id() == "456"
    user2 = User("xyz")
    assert user2.get_id() == "xyz"

def test_user_mixin_get_id_attribute_error_public():
    user = User(10)
    del user.id
    with pytest.raises(NotImplementedError):
        user.get_id()

def test_user_mixin_eq_true_public():
    user1 = User(55)
    user2 = User(55)
    assert user1 == user2

def test_user_mixin_eq_false_public():
    user1 = User(11)
    user2 = User(12)
    assert user1 != user2

def test_user_mixin_eq_type_public():
    user = User(222)
    assert (user == []) is False  # __eq__ returns NotImplemented, which Python converts to False

def test_user_mixin_ne_type_public():
    user = User(1234)
    assert (user != None) is True  # __ne__ returns NotImplemented, which Python converts to True

def test_user_mixin_hash_public():
    user = User(42)
    assert isinstance(hash(user), int)

def test_anonymous_user_mixin_properties_public():
    anon = AnonymousUserMixin()
    assert anon.is_active is False
    assert anon.is_authenticated is False
    assert anon.is_anonymous is True

def test_anonymous_user_mixin_get_id_public():
    anon = AnonymousUserMixin()
    assert anon.get_id() is None