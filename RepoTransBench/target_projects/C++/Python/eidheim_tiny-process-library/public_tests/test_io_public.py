import subprocess

def test_cat_echo():
    test_input = "public_test 123\nnewline"
    expected_output = test_input
    proc = subprocess.Popen(['cat'], stdin=subprocess.PIPE, stdout=subprocess.PIPE)
    out, err = proc.communicate(input=test_input.encode())
    assert out.decode() == expected_output

def test_grep_match():
    test_input = "apple\nbanana\norange\n"
    grep_pattern = "ban"
    expected = "banana\n"
    proc = subprocess.Popen(['grep', grep_pattern], stdin=subprocess.PIPE, stdout=subprocess.PIPE)
    out, err = proc.communicate(input=test_input.encode())
    assert out.decode() == expected

def test_grep_no_match():
    test_input = "dog\ncat\nmouse\n"
    grep_pattern = "tiger"
    expected = ""
    proc = subprocess.Popen(['grep', grep_pattern], stdin=subprocess.PIPE, stdout=subprocess.PIPE)
    out, err = proc.communicate(input=test_input.encode())
    assert out.decode() == expected