import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
import linkedin2username

def test_public_f_last():
    out = linkedin2username.f_last("Nina", "Simone")
    assert out == "nsimone"

def test_public_f_dot_last():
    out = linkedin2username.f_dot_last("Albert", "King")
    assert out == "a.king"

def test_public_last_f():
    out = linkedin2username.last_f("Armstrong", "Louis")
    assert out == "armstrongl"

def test_public_first_dot_last():
    out = linkedin2username.first_dot_last("Bessie", "Smith")
    assert out == "bessie.smith"

def test_public_first_l():
    out = linkedin2username.first_l("Duke", "Ellington")
    assert out == "dukee"

def test_public_first():
    out = linkedin2username.first_only("Ella", "Fitzgerald")
    assert out == "ella"

def test_public_clean_name():
    assert linkedin2username.clean_name(" Ray   Charles Jr.") == "ray charles jr"
    assert linkedin2username.clean_name("Dinah (CEO) Washington") == "dinah washington"
    assert linkedin2username.clean_name("Count Basie.") == "count basie"

def test_public_split_name():
    assert linkedin2username.split_name("Ruth Brown") == ("ruth", "brown", "")
    assert linkedin2username.split_name("Roy Orbison (VP)") == ("roy", "orbison", "")
    assert linkedin2username.split_name("Mr. Charles") == ("charles", "", "")

def test_public_find_employees():
    employees = [
        {"name": "Oscar Peterson"},
        {"name": "Sarah Vaughan"},
        {"name": "Mahalia Jackson"},
    ]
    # Should always find all, as actual function only returns matching list with 'name'
    found = linkedin2username.find_employees("dummy", employees)
    assert found == employees