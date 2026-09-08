import pytest

def test_listing_1_1_functional_print_message_with_new_data(monkeypatch):
    output = []
    monkeypatch.setattr("builtins.print", lambda s: output.append(s))
    def printToConsole(s):
        print(s)
        return s
    def toUpperCase(s):
        return s.upper()
    def echo(x):
        return x
    def run(*funcs):
        def composed(x):
            for f in reversed(funcs):
                x = f(x)
            return x
        return composed
    printMessage = run(printToConsole, toUpperCase, echo)
    assert printMessage('functional') == 'FUNCTIONAL'
    assert output[0] == 'FUNCTIONAL'

def test_listing_1_2_extending_print_message_with_new_data(monkeypatch):
    output = []
    monkeypatch.setattr("builtins.print", lambda s: output.append(s))
    def printToConsole(s):
        print(s)
        return s
    def toUpperCase(s):
        return s.upper()
    def echo(x):
        return x
    def repeat(times):
        def inner(s=''):
            return ' '.join([s for _ in range(times)])
        return inner
    def run(*funcs):
        def composed(x):
            for f in reversed(funcs):
                x = f(x)
            return x
        return composed
    printMessage = run(printToConsole, repeat(2), toUpperCase, echo)
    assert printMessage('public test') == 'PUBLIC TEST PUBLIC TEST'
    assert output[0] == 'PUBLIC TEST PUBLIC TEST'

def test_listing_1_3_imperative_show_student_function_with_side_effects_public_test(monkeypatch):
    output = []
    monkeypatch.setattr("builtins.print", lambda s: output.append(s))
    db = {
        '222-33-4444': {'ssn': '222-33-4444', 'firstname': 'Ada', 'lastname': 'Lovelace'}
    }
    def showStudent(ssn):
        student = db.get(ssn)
        if student is not None:
            studentInfo = f"<p>{student['ssn']},{student['firstname']},{student['lastname']}</p>"
            print(studentInfo)
            return studentInfo
        else:
            raise Exception('Student not')
    assert showStudent('222-33-4444') == '<p>222-33-4444,Ada,Lovelace</p>'
    assert output[0] == '<p>222-33-4444,Ada,Lovelace</p>'

def test_listing_1_4_decomposing_show_student_program_public():
    output = []
    import builtins
    orig_print = builtins.print
    builtins.print = lambda x: output.append(x)
    db = {
        '333-22-1111': {'ssn': '333-22-1111', 'firstname': 'Grace', 'lastname': 'Hopper'}
    }
    def find(dbinst, id):
        obj = dbinst.get(id)
        if obj is None:
            raise Exception('Object not found!')
        return obj
    def csv(student):
        return f"{student['ssn']}, {student['firstname']}, {student['lastname']}"
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
    showStudent = run(append(print), csv, lambda x: find(db, x))
    try:
        assert showStudent('333-22-1111') == '333-22-1111, Grace, Hopper'
        assert output[0] == '333-22-1111, Grace, Hopper'
    finally:
        builtins.print = orig_print

def test_listing_1_5_programming_with_function_chains_public(monkeypatch):
    output = []
    monkeypatch.setattr("builtins.print", lambda s: output.append(s))
    enrollments = [
        {'enrolled': 2, 'grade': 75},
        {'enrolled': 1, 'grade': 65},
        {'enrolled': 3, 'grade': 85},
    ]
    filtered = [student for student in enrollments if student['enrolled'] > 1]
    grades = [student['grade'] for student in filtered]
    result = sum(grades) / len(grades) if grades else 0
    print(result)
    assert result == 80
    assert output[0] == 80