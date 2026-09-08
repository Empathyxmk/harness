def is_sorted(lst):
    return all(lst[i] <= lst[i+1] for i in range(len(lst)-1))

def test_public_sorted_positive():
    assert is_sorted([0,1,2,3,4])

def test_public_sorted_negative():
    assert not is_sorted([5,4,3])

def test_public_sorted_single():
    assert is_sorted([10])