import pytest

from code_examples.create_tests_via_parametrization.foobar import Man, Woman, Package

@pytest.fixture(params=['matplotlib', 'pandas'])
def public_python_package(request):
    return Package(request.param)

@pytest.mark.parametrize('person', [
    Man('Oliver'), Woman('Amelia'),
    Man('Mason'), Man('Logan'), Woman('Harper')
])
def test_become_a_programmer_public(person, public_python_package):
    person.learn(public_python_package.name)
    assert person.looks_like_a_programmer

@pytest.mark.parametrize('person', [
    Man('Jack'),
    Woman('Lily')
])
def test_learn_multiple_packages_public(person):
    person.learn('sqlalchemy')
    person.learn('httpx')
    assert person.looks_like_a_programmer

@pytest.mark.parametrize('person', [
    Man('Henry'),
    Woman('Ella')
])
def test_not_programmer_initially_public(person):
    assert not person.looks_like_a_programmer