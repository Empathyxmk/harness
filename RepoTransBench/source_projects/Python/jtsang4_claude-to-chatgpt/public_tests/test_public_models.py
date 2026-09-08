import claude_to_chatgpt.models as models

def test_public_models_list_exists():
    # List should exist and be iterable, but check different property
    assert hasattr(models.models_list, "__iter__")
    assert all(isinstance(item, str) for item in models.models_list)

def test_public_model_map_exists():
    # Dict should exist and contain at least one mapping
    assert hasattr(models.model_map, "items")
    assert all(isinstance(k, str) and isinstance(v, str) for k, v in models.model_map.items())