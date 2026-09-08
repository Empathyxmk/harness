import pytest

class PositiveNumberPredicate:
    def test(self, number):
        return number > 0

@pytest.mark.parametrize("name,func", [
    ("Add test", lambda: assert_true(True)),
    ("Multiply Test", lambda: assert_true(True)),
])
def test_dynamic_tests_with_collection(request, name, func):
    func()

def assert_true(expr):
    assert expr

def test_dynamic_tests_with_iterator():
    for func in [lambda: assert_true(True), lambda: assert_true(True)]:
        func()

def test_dynamic_tests_with_stream():
    for func in [lambda: assert_true(True), lambda: assert_true(True)]:
        func()

@pytest.mark.parametrize("number", [-1, 0, 1])
def test_dynamic_tests_from_int_stream(number):
    predicate = PositiveNumberPredicate()
    if number > 0:
        assert predicate.test(number)
    else:
        assert not predicate.test(number)

@pytest.mark.parametrize("text", ["foo", "bar", "baz"])
def test_dynamic_tests_from_lambda(text):
    assert len(text) > 0

def test_generate_random_number_of_tests():
    for _ in range(5):
        assert True

@pytest.mark.parametrize("number", [1, 0, -1, 5, -3])
def test_dynamic_tests_for_positive_number_predicate(number):
    predicate = PositiveNumberPredicate()
    if number > 0:
        assert predicate.test(number)
    else:
        assert not predicate.test(number)