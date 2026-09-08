import pytest
from src.dmoulding_boilermake.animal import Cat, Dog, Mouse, Chihuahua

# These tests match the extra methods used in the public test C++
# Check name, age, breed, and speak() for each derived class.

def test_cat_public():
    cat = Cat("Garfield", 4)
    assert cat.get_name() == "Garfield"
    assert cat.get_age() == 4
    assert cat.speak() == "Meow! I am Garfield!"

def test_dog_public():
    dog = Dog("Max", 7)
    assert dog.get_name() == "Max"
    assert dog.get_age() == 7
    assert dog.speak() == "Woof! I am Max!"

def test_mouse_public():
    mouse = Mouse("Speedy", 2)
    assert mouse.get_name() == "Speedy"
    assert mouse.get_age() == 2
    assert mouse.speak() == "Squeak! I'm Speedy!"

def test_chihuahua_public():
    chihuahua = Chihuahua("Coco", 6, "Mini")
    assert chihuahua.get_name() == "Coco"
    assert chihuahua.get_age() == 6
    assert chihuahua.get_breed() == "Mini"
    assert chihuahua.speak() == "Yip! I am Coco the Mini Chihuahua!"