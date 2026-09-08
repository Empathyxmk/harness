import pytest

"""
Patterned on test_override.cpp, but with different logic/data.
"""

class Animal:
    def sound(self):
        return "unknown"

class Cat(Animal):
    def sound(self):
        return "meow"

class Dog(Animal):
    def sound(self):
        return "woof"

def test_cat():
    c = Cat()
    a = c
    assert a.sound() == "meow"

def test_dog():
    d = Dog()
    a = d
    assert a.sound() == "woof"