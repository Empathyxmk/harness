import pytest

def iota(arr):
    count = 0
    for i in range(len(arr)):
        arr[i] = count
        count += 1

def test_array_basic_print(capsys):
    a = [2, 1, 0]
    for ai in a:
        print(ai)
    iota(a)
    for ai in a:
        print(ai)
    print(f"front:{a[0]}")
    print(f"back:{a[-1]}")
    for ai in reversed(a):
        print(ai, end=' ')
    print()
    captured = capsys.readouterr()
    out_lines = captured.out.strip().splitlines()
    # Test that iota set the array to consecutive numbers
    assert out_lines[3:6] == ['0', '1', '2']
    # front and back print
    assert out_lines[6] == "front:0"
    assert out_lines[7] == "back:2"
    # Last line should be: "2 1 0"
    assert out_lines[-1].strip() == "2 1 0"