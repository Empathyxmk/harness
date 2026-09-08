def entity(name, fields):
    class Entity:
        def __init__(self, **kwargs):
            self.meta = type('Meta', (), {})()
            self.meta.name = name
            for k, v in kwargs.items():
                setattr(self, k, v)
    return Entity

def field(_type):
    return _type

def id(_type):
    return _type

def given_another_entity():
    AnotherEntity = entity('Another entity', {
        'altField1': field(int),
        'altField2': id(int)
    })
    return AnotherEntity()

def test_should_initiate_with_public_data():
    instance = given_another_entity()
    assert instance.meta.name == 'Another entity'