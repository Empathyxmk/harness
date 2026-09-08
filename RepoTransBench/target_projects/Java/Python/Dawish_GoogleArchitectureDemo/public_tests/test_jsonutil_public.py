import json

class Animal:
    def __init__(self, type, age):
        self.type = type
        self.age = age

    def __eq__(self, other):
        return (
            isinstance(other, Animal)
            and self.type == other.type
            and self.age == other.age
        )

def str2jsonbean(json_str, cls):
    try:
        d = json.loads(json_str)
        return cls(**d)
    except Exception:
        return None

def jsonbean2str(obj):
    try:
        return json.dumps(obj.__dict__)
    except Exception:
        return None

def jsonlist2str(lst):
    try:
        return json.dumps([o.__dict__ for o in lst])
    except Exception:
        return None

def test_str2jsonbean_with_different_data():
    animal_json = '{"type":"Dog","age":4}'
    animal = str2jsonbean(animal_json, Animal)
    assert animal is not None
    assert animal.type == "Dog"
    assert animal.age == 4

def test_jsonbean2str_with_different_data():
    animal = Animal("Cat", 2)
    json_str = jsonbean2str(animal)
    assert "\"type\":\"Cat\"" in json_str or '"type": "Cat"' in json_str
    assert "\"age\":2" in json_str or '"age": 2' in json_str

def test_jsonlist2str_with_different_data():
    animal_list = [Animal("Horse", 7), Animal("Rabbit", 1)]
    json_str = jsonlist2str(animal_list)
    assert json_str.startswith("[")
    assert '"type":"Horse"' in json_str or '"type": "Horse"' in json_str
    assert '"type":"Rabbit"' in json_str or '"type": "Rabbit"' in json_str
    assert json_str.endswith("]")