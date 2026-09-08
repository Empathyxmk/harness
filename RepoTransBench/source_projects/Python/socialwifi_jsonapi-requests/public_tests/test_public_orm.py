import pytest
from jsonapi_requests.orm import api_model, fields, registry, repositories

# Use the correct available fields: String, Integer, etc.
class MyPublicModel(api_model.ApiModel):
    name = fields.String()
    age = fields.Integer()

@pytest.fixture
def model_registry():
    reg = registry.Registry()
    reg.register(MyPublicModel)
    return reg

def test_public_model_fields(model_registry):
    # Use different data from original (different name/age)
    obj = MyPublicModel(name="Alice Wonderland", age=35)
    assert obj.name == "Alice Wonderland"
    assert obj.age == 35

def test_public_model_update_fields():
    obj = MyPublicModel(name="Bob Builder", age=44)
    obj.name = "Bobby"
    obj.age = 45
    assert obj.name == "Bobby"
    assert obj.age == 45

def test_public_model_repository(model_registry):
    repo = repositories.InMemoryRepository(MyPublicModel)
    # Add with different values than original tests
    obj = MyPublicModel(name="Charlie Delta", age=27)
    repo.save(obj)
    found = repo.get(obj.id)
    assert found.name == "Charlie Delta"
    assert found.age == 27
    all_objs = list(repo.all())
    assert any(o.name == "Charlie Delta" and o.age == 27 for o in all_objs)