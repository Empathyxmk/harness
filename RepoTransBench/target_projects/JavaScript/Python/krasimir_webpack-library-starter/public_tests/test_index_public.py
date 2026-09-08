from src import index
from src.cat import Cat
from src.dog import Dog

def test_bundle_cat_and_dog_as_functions():
    # In Python, classes are types.
    assert isinstance(index.Cat, type)
    assert isinstance(index.Dog, type)

def test_bundle_cat_dog_distinct_names_and_types():
    assert index.Cat.__name__ == "Cat"
    assert index.Dog.__name__ == "Dog"
    assert index.Cat is not list
    assert index.Dog is not dict

def test_bundle_cat_instance_equality_and_type():
    bundleCat = index.Cat()
    localCat = Cat()
    assert bundleCat.name == localCat.name
    assert isinstance(bundleCat, Cat)
    assert isinstance(bundleCat, index.Cat)

def test_bundle_dog_instance_equality_and_type():
    bundleDog = index.Dog()
    localDog = Dog()
    assert bundleDog.name == localDog.name
    assert isinstance(bundleDog, Dog)
    assert isinstance(bundleDog, index.Dog)