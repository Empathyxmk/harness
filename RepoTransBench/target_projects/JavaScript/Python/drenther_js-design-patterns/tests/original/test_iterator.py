def import_iterator():
    from src.Behavioral.Iterator import IteratorClass, iterator_using_generator
    return IteratorClass, iterator_using_generator

def test_iterator_class_iterates_correctly():
    IteratorClass, _ = import_iterator()
    data = [1, 2, 3]
    iterator = IteratorClass(data)
    result = [item for item in iterator]
    assert result == data

def test_iterator_class_iterates_again_after_finishing():
    IteratorClass, _ = import_iterator()
    data = ['a', 'b']
    iterator = IteratorClass(data)
    result1 = [item for item in iterator]
    result2 = [item for item in iterator]
    assert result1 == data
    assert result2 == data

def test_generator_yields_all_items_in_order():
    _, iterator_using_generator = import_iterator()
    data = [5, 6, 7]
    gen = iterator_using_generator(data)
    assert list(gen) == data

def test_generator_on_empty_array_yields_nothing():
    _, iterator_using_generator = import_iterator()
    data = []
    gen = iterator_using_generator(data)
    assert list(gen) == []