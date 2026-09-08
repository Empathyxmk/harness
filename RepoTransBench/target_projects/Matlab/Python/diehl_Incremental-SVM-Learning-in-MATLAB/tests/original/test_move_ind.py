import pytest

def move_ind(inda, indb, indc):
    """Remove all elements of inda that are in indc, append indc to indb."""
    inda = list(inda)
    indb = list(indb)
    indc = list(indc)
    # Remove all occurrences in inda that match any in indc
    new_inda = [i for i in inda if i not in indc]
    new_indb = indb + indc
    return new_inda, new_indb

def test_basic_move():
    inda = [1, 2, 3, 4, 5]
    indb = [10, 11]
    indc = [2, 4]
    new_inda, new_indb = move_ind(inda, indb, indc)
    assert new_inda == [1, 3, 5]
    assert new_indb == [10, 11, 2, 4]

def test_move_all():
    inda = [1,2,3]
    indb = [10]
    indc = [1,2,3]
    new_inda, new_indb = move_ind(inda, indb, indc)
    assert new_inda == []
    assert new_indb == [10,1,2,3]

def test_move_none():
    inda = [1,2,3]
    indb = [10]
    indc = []
    new_inda, new_indb = move_ind(inda, indb, indc)
    assert new_inda == inda
    assert new_indb == indb

def test_no_overlap():
    inda = [1,2,3]
    indb = [10]
    indc = [4,5]
    new_inda, new_indb = move_ind(inda, indb, indc)
    assert new_inda == inda
    assert new_indb == [10,4,5]

def test_duplicates_in_indc():
    inda = [1,2,2,3]
    indb = [10]
    indc = [2,2]
    new_inda, new_indb = move_ind(inda, indb, indc)
    assert new_inda == [1,3]
    assert new_indb == [10,2,2]