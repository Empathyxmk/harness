import pytest
from src.profile import Profile, ProfileList, StrLower, IsSameProfile, CleanProfile, ValidProfile, CopyProfile

def test_StrLower_extra_public():
    s2 = "ZZ"
    assert StrLower(s2) == "zz"
    s3 = "MiXeDCaSe"
    assert StrLower(s3) == "mixedcase"
    s4 = "123abcDEF!$*"
    assert StrLower(s4) == "123abcdef!$*"

def test_IsSameProfile_edge_public():
    pa = Profile(1001, "epsilon")
    pb = Profile(1001, "omicron")
    pc = Profile(1002, "epsilon")
    assert IsSameProfile(pa, pb)
    assert not IsSameProfile(pa, pc)

def test_CleanProfile_and_ValidProfile_public():
    pclean = Profile(7, "xyz")
    CleanProfile(pclean)
    assert pclean.id == 0 and pclean.name == "" and not ValidProfile(pclean)
    pvalid = Profile(11, "")
    pvalid.name = "A"
    assert ValidProfile(pvalid)
    pvalid.id = 0
    assert not ValidProfile(pvalid)

def test_CopyProfile_diff_public():
    src = Profile(18, "DST")
    dest = Profile(4242, "")
    CopyProfile(dest, src)
    assert dest.id == 18 and dest.name == "DST"

def test_ProfileList_Insert_public():
    pl2 = ProfileList()
    for i in range(10, 18):
        tmp = Profile(i * 2, "Goo")
        pl2.InsertProfile(tmp)
    before = pl2.count
    ovr = Profile(99999, "NoRoom")
    pl2.InsertProfile(ovr)
    assert pl2.count == before

def test_ProfileList_SearchProfile_public():
    pl2 = ProfileList()
    for i in range(10, 18):
        tmp = Profile(i * 2, "Goo")
        pl2.InsertProfile(tmp)
    idx1 = pl2.SearchProfile(20)
    assert idx1 == 0
    idx2 = pl2.SearchProfile(424242)
    assert idx2 == -1

def test_CleanProfile_already_clean_public():
    zero = Profile()
    CleanProfile(zero)
    assert zero.id == 0 and zero.name == ""