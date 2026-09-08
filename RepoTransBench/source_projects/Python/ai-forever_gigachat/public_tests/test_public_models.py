import pytest

# Try importing Model from both possible locations depending on project src layout:
try:
    from src.gigachat.model import Model
except ImportError:
    try:
        from gigachat.model import Model
    except ImportError:
        Model = None  # Will be handled in test skip

@pytest.mark.skipif(Model is None, reason="Model class not found")
def test_model_init_and_fields():
    # Provide all required fields: object, id, created, name, owned_by
    model = Model(
        object="special_object",
        id="test_id_2",
        created=1234567,
        name="SuperGigaModel",
        owned_by="public_giga_owner"
    )
    assert model.id == "test_id_2"
    assert model.object == "special_object"
    assert model.name == "SuperGigaModel"
    assert model.owned_by == "public_giga_owner"
    assert isinstance(model.created, int)
    # x_headers is optional, should default to None
    assert getattr(model, "x_headers", None) is None

@pytest.mark.skipif(Model is None, reason="Model class not found")
def test_model_str_and_repr_public():
    model = Model(
        object="public_object",
        id="AAA_public",
        created=1010101,
        name="PublicModel",
        owned_by="someone_else"
    )
    # The __str__ and __repr__ should include at least id or name (customize check as per Model)
    text = str(model)
    rep = repr(model)
    assert "AAA_public" in text or "PublicModel" in text
    assert "AAA_public" in rep or "PublicModel" in rep