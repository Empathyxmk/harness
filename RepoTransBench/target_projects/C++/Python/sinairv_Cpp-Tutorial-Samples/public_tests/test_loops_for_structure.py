import pytest

def test_loops_for_structure_output(capsys):
    """
    Public test: Output numbers from 5 to 15 using a for loop
    """
    # Python equivalent for (int i=5; i<=15; i++) { cout << i << endl; }
    for i in range(5, 16):
        print(i)
    # Capture and verify output
    captured = capsys.readouterr()
    expected_lines = [f"{i}\n" for i in range(5, 16)]
    assert captured.out == ''.join(expected_lines)