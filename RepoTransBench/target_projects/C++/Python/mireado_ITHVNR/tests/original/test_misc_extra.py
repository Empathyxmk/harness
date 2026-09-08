import pytest
from src.profile import Profile, ProfileList, StrLower, IsSameProfile, CleanProfile, ValidProfile, CopyProfile

def test_StrLower_extra():
    s2 = ""
    assert StrLower(s2) == ""
    s3 = "already"
    assert StrLower(s3) == "already"
    s4 = "ABC123!@#"
    assert StrLower(s4) == "abc123!@#"

def test_IsSameProfile_edge():
    pa = Profile(11, "Alpha")
    pb = Profile(11, "Beta")
    pc = Profile(12, "Alpha")
    assert IsSameProfile(pa, pb)
    assert not IsSameProfile(pa, pc)

def test_CleanProfile_and_ValidProfile():
    pclean = Profile(99, "Populated")
    CleanProfile(pclean)
    assert pclean.id == 0 and pclean.name == "" and not ValidProfile(pclean)
    pvalid = Profile(1, "")
    pvalid.name = "Y"
    assert ValidProfile(pvalid)
    pvalid.id = 0
    assert not ValidProfile(pvalid)

def test_CopyProfile_diff_source_dest_order():
    src = Profile(88, "Source")
    dest = Profile()
    CopyProfile(dest, src)
    assert dest.id == 88 and dest.name == "Source"

def test_ProfileList_Insert_edge():
    pl2 = ProfileList()
    for i in range(8):
        tmp = Profile(i+1, "Fill")
        pl2.InsertProfile(tmp)
    before = pl2.count
    ovr = Profile(999, "Full")
    pl2.InsertProfile(ovr)
    assert pl2.count == before

def test_ProfileList_SearchProfile_present_not_present_first_entry():
    pl2 = ProfileList()
    for i in range(8):
        tmp = Profile(i+1, "Fill")
        pl2.InsertProfile(tmp)
    idx1 = pl2.SearchProfile(1)
    assert idx1 == 0
    idx2 = pl2.SearchProfile(9999)
    assert idx2 == -1

def test_CleanProfile_already_clean():
    zero = Profile()
    CleanProfile(zero)
    assert zero.id == 0 and zero.name == ""