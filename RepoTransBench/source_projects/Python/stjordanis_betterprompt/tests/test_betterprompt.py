import betterprompt

def test_metadata():
    assert isinstance(betterprompt.__version__, str)
    assert isinstance(betterprompt.__author__, str)
    assert isinstance(betterprompt.__copyright__, str)
    assert isinstance(betterprompt.__license__, str)
    assert "get_from_dict_or_env" in betterprompt.__all__

def test_dummy_openai_completion_create():
    result = betterprompt.DummyOpenAICompletion.create()
    assert isinstance(result, dict)
    assert "choices" in result

def test_openai_completion_static(monkeypatch):
    old_class = betterprompt.openai.Completion
    try:
        class DummyCompletion:
            @staticmethod
            def create(*args, **kwargs):
                return {"choices": [{"logprobs": {"token_logprobs": [0.5]}}]}
        monkeypatch.setattr(betterprompt.openai, "Completion", DummyCompletion)
        res = betterprompt.openai.Completion.create()
        assert res["choices"][0]["logprobs"]["token_logprobs"] == [0.5]
    finally:
        betterprompt.openai.Completion = old_class