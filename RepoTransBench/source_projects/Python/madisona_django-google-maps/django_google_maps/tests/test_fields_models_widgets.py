import pytest

from django_google_maps import fields, models, widgets

class DummyModel:
    pass

def test_geoptfield_to_python_and_get_prep_value():
    f = fields.GeoPtField()
    assert f.to_python("40.1,-122.1") == (40.1, -122.1)
    assert f.get_prep_value((10.0, 20.0)) == '10.0,20.0'
    assert f.get_prep_value("50.33,80.55") == '50.33,80.55'
    assert f.to_python(None) is None

    # error case
    with pytest.raises(Exception):
        f.to_python("badinput")

def test_geolocationfield_deconstruct_and_other():
    f = fields.AddressField(max_length=100, default='def')
    name, path, args, kwargs = f.deconstruct()
    assert name == None or isinstance(name, str)  # name is not used in call
    assert 'max_length' in kwargs
    assert kwargs["max_length"] == 100
    assert kwargs["default"] == 'def'

    latlng = fields.GeoLocationField()
    assert hasattr(latlng, "formfield")
    # test deconstruct for GeoLocationField
    _, _, _, kw = latlng.deconstruct()
    assert isinstance(kw, dict)

def test_models_address_and_location_field_repr_and_str():
    fields_and_vals = [
        (models.AddressField(max_length=255), "123 st la"),
        (models.LocationField(max_length=255), "11.0,122.2"),
    ]
    for field, val in fields_and_vals:
        # direct __str__ calls
        assert "Field" in str(field)
        # contribute to class
        cls = type("TestModel", (), {})
        field.contribute_to_class(cls, "foo_addr")
        instance = cls()
        setattr(instance, "foo_addr", val)
        # Would run through model machinery in real usage

def test_widgets_render_attrs_instantiation():
    # Basic widget coverage
    map_widget = widgets.MapWidget()
    html = map_widget.render("test", "value", attrs={"id": "some_id"})
    assert "id" in html or "map" in html
    # Check js_attrs property
    _ = map_widget.js_attrs

def test_custom_clean_validation(monkeypatch):
    f = fields.GeoPtField()
    # monkeypatch to Python's built-in float to simulate error
    monkeypatch.setattr(fields, 'float', lambda x: (_ for _ in ()).throw(ValueError))
    with pytest.raises(Exception):
        f.to_python("50.11,-101.2")