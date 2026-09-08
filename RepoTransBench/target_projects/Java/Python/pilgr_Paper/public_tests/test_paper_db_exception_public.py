from src.paperdb.exceptions import PaperDbException

def test_message_constructor_public():
    ex = PaperDbException("fail-public")
    assert str(ex) == "fail-public"

def test_message_and_throwable_constructor_public():
    t = Exception("public-cause")
    ex = PaperDbException("fail-public2")
    ex.__cause__ = t
    assert str(ex) == "fail-public2"
    assert ex.__cause__ == t