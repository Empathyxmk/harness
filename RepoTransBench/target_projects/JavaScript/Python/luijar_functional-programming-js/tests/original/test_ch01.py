import pytest

# Utilities for test mocking
class DummyDB:
    def find(self, ssn):
        if ssn in ('444-44-4444', '444444444'):
            class Person:
                def __init__(self):
                    self.ssn = '444-44-4444'
                    self.firstname = 'Alonzo'
                    self.lastname = 'Church'
            return Person()
        return None

@pytest.fixture
def db():
    return DummyDB()

def test_listing_1_1_functional_print_message(monkeypatch):
    output = []
    monkeypatch.setattr("builtins.print", lambda s: output.append(s))
    def printToConsole(str):
        print(str)
        return str
    def toUpperCase(str):
        return str.upper()
    def echo(x):
        return x

    def run(*funcs):
        def composed(x):
            for f in reversed(funcs):
                x = f(x)
            return x
        return composed

    printMessage = run(printToConsole, toUpperCase, echo)
    assert printMessage('Hello World') == 'HELLO WORLD'
    assert output[0] == 'HELLO WORLD'

def test_listing_1_2_extending_print_message(monkeypatch):
    output = []
    monkeypatch.setattr("builtins.print", lambda s: output.append(s))
    def printToConsole(str):
        print(str)
        return str
    def toUpperCase(str):
        return str.upper()
    def echo(x):
        return x
    def repeat(times):
        def inner(str=''):
            return ' '.join([str for _ in range(times)])
        return inner

    def run(*funcs):
        def composed(x):
            for f in reversed(funcs):
                x = f(x)
            return x
        return composed

    printMessage = run(printToConsole, repeat(3), toUpperCase, echo)
    res = printMessage('Hello World')
    assert res == 'HELLO WORLD HELLO WORLD HELLO WORLD'
    assert output[0] == 'HELLO WORLD HELLO WORLD HELLO WORLD'

def test_listing_1_3_imperative_show_student_function_with_side_effects(db, monkeypatch):
    output = []
    monkeypatch.setattr("builtins.print", lambda s: output.append(s))
    def showStudent(ssn):
        student = db.find(ssn)
        if student is not None:
            studentInfo = f"<p>{student.ssn},{student.firstname},{student.lastname}</p>"
            print(studentInfo)
            return studentInfo
        else:
            raise Exception('Student not')
    assert showStudent('444-44-4444') == '<p>444-44-4444,Alonzo,Church</p>'

def test_listing_1_4_decomposing_show_student_program(db, monkeypatch):
    output = []
    monkeypatch.setattr("builtins.print", lambda s: output.append(s))
    def curry(fn):
        def curried1(x, y=None):
            return lambda y2: fn(x, y2) if y is None else fn(x, y)
        return curried1
    def find(dbinst, id):
        obj = dbinst.find(id)
        if obj is None:
            raise Exception('Object not found!')
        return obj
    find_curried = lambda db: lambda id: find(db, id)
    def csv(student):
        return f"{student.ssn}, {student.firstname}, {student.lastname}"
    def append(source):
        def inner(info):
            source(info)
            return info
        return inner
    def run(*funcs):
        def composed(x):
            for f in reversed(funcs):
                x = f(x)
            return x
        return composed
    showStudent = run(append(print), csv, find_curried(db))
    assert showStudent('444-44-4444') == '444-44-4444, Alonzo, Church'

def test_listing_1_5_programming_with_function_chains(monkeypatch):
    output = []
    monkeypatch.setattr("builtins.print", lambda s: output.append(s))
    enrollments = [
        {'enrolled': 3, 'grade': 90},
        {'enrolled': 1, 'grade': 100},
        {'enrolled': 1, 'grade': 87}
    ]
    result = (
        sum([student['grade'] for student in enrollments if student['enrolled'] > 1]) /
        len([student['grade'] for student in enrollments if student['enrolled'] > 1])
        if len([student['grade'] for student in enrollments if student['enrolled'] > 1]) > 0 else 0
    )
    print(result)
    assert result == 90
    assert output[0] == 90