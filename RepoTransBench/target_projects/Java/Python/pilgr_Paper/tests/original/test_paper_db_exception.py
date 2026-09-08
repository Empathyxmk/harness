from src.paperdb.exceptions import PaperDbException

def test_message_constructor():
    ex = PaperDbException("fail")
    assert str(ex) == "fail"

def test_message_and_throwable_constructor():
    t = Exception("t cause")
    ex = PaperDbException("fail2")
    ex.__cause__ = t
    assert str(ex) == "fail2"
    assert ex.__cause__ == t