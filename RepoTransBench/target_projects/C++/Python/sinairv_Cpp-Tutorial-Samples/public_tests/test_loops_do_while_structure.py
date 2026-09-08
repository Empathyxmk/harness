import pytest

def test_loops_do_while_structure_output(capsys):
    """
    Public test: Output numbers from 20 to 29 using a do-while loop
    """
    # C++: int i = 20; do { cout << i << endl; i++; } while(i < 30);
    i = 20
    while True:
        print(i)
        i += 1
        if i >= 30:
            break
    # Capture and verify output
    captured = capsys.readouterr()
    expected_lines = [f"{j}\n" for j in range(20, 30)]
    assert captured.out == ''.join(expected_lines)