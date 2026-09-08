def import_prototype():
    from src.Creational.Prototype import car
    return car

def test_create_object_with_prototype():
    car = import_prototype()
    # In JS: Object.create(car, { owner: { value: 'John' } });
    # In Python: use type + property set
    class MyCar(car.__class__):
        pass
    my_car = MyCar()
    my_car.__dict__ = car.__dict__.copy()
    my_car.owner = 'John'
    assert getattr(my_car, 'no_of_wheels', None) == 4
    assert my_car.start() == 'started'
    assert my_car.stop() == 'stopped'
    assert my_car.owner == 'John'
    # __proto__ equivalent in Python is seldom compared directly, but:
    assert my_car.__class__.__bases__[0] == car.__class__