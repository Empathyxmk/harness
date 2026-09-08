import sys

def test_case_study_3_tuple_type_identity(capsys):
    # Mimic tuple type usage in C++
    # C++ code:
    # using my_tuple = tuple<double, char, float>;
    # elt_0 = at<0, my_tuple>
    # cout << is_same<elt_0, float>::value << endl; // should print 0 (not float)
    # elt_2 = at<2, my_tuple>
    # cout << is_same<elt_2, float>::value << endl; // should print 1 (is float)
    
    # For Python, index 0 should not be float (simulate 'double'), index 2 should be float.
    types = [complex, str, float]  # simulate: double, char, float
    # is_same[0] to float: should be False
    # is_same[2] to float: should be True

    print(int(types[0] is float))  # should print 0
    print(int(types[2] is float))  # should print 1

    captured = capsys.readouterr().out.strip().split('\n')
    assert captured[0].strip() == "0"
    assert captured[1].strip() == "1"