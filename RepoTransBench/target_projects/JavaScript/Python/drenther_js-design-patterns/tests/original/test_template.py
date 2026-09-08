import pytest

def import_template():
    from src.Behavioral.Template import Developer, Tester
    return Developer, Tester

def test_developer_responsibilities_and_pay():
    Developer, _ = import_template()
    dev = Developer('Alice', 1500)
    assert dev.work() == 'Alice handles application development'
    assert dev.get_paid() == 'Alice got paid 1500'

def test_tester_responsibilities_and_pay():
    _, Tester = import_template()
    qa = Tester('Bob', 900)
    assert qa.work() == 'Bob handles testing'
    assert qa.get_paid() == 'Bob got paid 900'

def test_developer_responsibility_method_override():
    Developer, _ = import_template()
    class CustomDev(Developer):
        def responsibilities(self):
            return 'custom stuff'
    c_dev = CustomDev('Eve', 1200)
    assert c_dev.work() == 'Eve handles custom stuff'