import pytest
from src.profile import Profile, ProfileList, StrLower, IsSameProfile, CleanProfile, ValidProfile, CopyProfile

def test_StrLower_public():
    s1 = "ExamPLE"
    assert StrLower(s1) == "example"
    assert StrLower(None) is None

def test_IsSameProfile_public():
    p1 = Profile(21, "Alpha")
    p2 = Profile(21, "Alpha")
    p3 = Profile(98, "Beta")
    assert IsSameProfile(p1, p2)
    assert not IsSameProfile(p1, p3)
    assert not IsSameProfile(None, p2)
    assert not IsSameProfile(p1, None)

def test_CleanProfile_public():
    p4 = Profile(73, "PublicTest")
    CleanProfile(p4)
    assert p4.id == 0
    assert p4.name == ""
    CleanProfile(None)  # Should not raise

def test_ValidProfile_public():
    p5 = Profile(33, "FooBar")
    p6 = Profile(0, "none")
    assert ValidProfile(p5)
    assert not ValidProfile(p6)
    assert not ValidProfile(None)

def test_CopyProfile_public():
    src = Profile(45, "CopyTest")
    dst = Profile()
    CopyProfile(dst, src)
    assert dst.id == 45 and dst.name == "CopyTest"
    CopyProfile(None, src)
    CopyProfile(dst, None)

def test_ProfileList_Insert_and_Search_public():
    pl = ProfileList()
    for i in range(11, 19):
        tmp = Profile(i, "Q")
        pl.InsertProfile(tmp)
    assert pl.count == 8
    over = Profile(42, "NotInserted")
    pl.InsertProfile(over)
    assert pl.count == 8
    idx = pl.SearchProfile(15)
    assert idx == 4
    notfound = pl.SearchProfile(200)
    assert notfound == -1