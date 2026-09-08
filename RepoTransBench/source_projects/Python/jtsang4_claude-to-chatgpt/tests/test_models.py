import claude_to_chatgpt.models as models

def test_models_list_exists():
    assert type(models.models_list) == list

def test_model_map_exists():
    assert type(models.model_map) == dict