def move_ind(arr, from_idx, to_idx):
    arr = list(arr)
    # Convert 1-based MATLAB to 0-based Python: indices
    from_idx -= 1
    to_idx -= 1
    # Remove the element to move
    val = arr.pop(from_idx)
    arr.insert(to_idx, val)
    return arr

def test_public_move_ind():
    arr = [7,8,9,0,1,2]
    from_idx = 6 # last element (Matlab 1-based: 6 == Python 5)
    to_idx = 2   # 2nd position
    expected = [7,2,8,9,0,1]
    actual = move_ind(arr, from_idx, to_idx)
    assert expected == actual