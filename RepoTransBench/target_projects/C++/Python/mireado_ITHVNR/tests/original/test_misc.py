import pytest
from src.profile import Profile, ProfileList, StrLower, IsSameProfile, CleanProfile, ValidProfile, CopyProfile

def test_StrLower():
    s1 = "TesT"
    assert StrLower(s1) == "test"
    assert StrLower(None) is None

def test_IsSameProfile():
    p1 = Profile(1, "One")
    p2 = Profile(1, "One")
    p3 = Profile(2, "Two")
    assert IsSameProfile(p1, p2)
    assert not IsSameProfile(p1, p3)
    assert not IsSameProfile(None, p2)
    assert not IsSameProfile(p1, None)

def test_CleanProfile():
    p4 = Profile(42, "Cleanup")
    CleanProfile(p4)
    assert p4.id == 0
    assert p4.name == ""
    CleanProfile(None)  # Should not raise

def test_ValidProfile():
    p5 = Profile(5, "Valid")
    p6 = Profile(0, "Invalid")
    assert ValidProfile(p5)
    assert not ValidProfile(p6)
    assert not ValidProfile(None)

def test_CopyProfile():
    src = Profile(7, "Copy")
    dst = Profile()
    CopyProfile(dst, src)
    assert dst.id == 7 and dst.name == "Copy"
    CopyProfile(None, src)  # Should not raise
    CopyProfile(dst, None)  # Should not raise

def test_ProfileList_Insert_and_Search():
    pl = ProfileList()
    for i in range(1, 9):
        tmp = Profile(i, "P")
        pl.InsertProfile(tmp)
    assert pl.count == 8
    over = Profile(99, "ShouldNotAdd")
    pl.InsertProfile(over)
    assert pl.count == 8
    idx = pl.SearchProfile(5)
    assert idx == 4
    notfound = pl.SearchProfile(100)
    assert notfound == -1