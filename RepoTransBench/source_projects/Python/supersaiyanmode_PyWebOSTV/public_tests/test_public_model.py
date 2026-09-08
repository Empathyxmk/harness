import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from pywebostv import model

def test_device_model_public():
    # Use different test data
    info = {
        "capabilities": {
            "list": ["PublicCapability1", "PublicCapability2"]
        },
        "modelName": "PublicLG123",
        "friendlyName": "Public TV",
        "udn": "Public-UUID"
    }
    device = model.Device(info)
    assert device.capabilities == {"list": ["PublicCapability1", "PublicCapability2"]}
    assert device.model_name == "PublicLG123"
    assert device.name == "Public TV"
    assert device.uuid == "Public-UUID"

def test_application_public():
    data = {
        "id": "app.public",
        "title": "Public App",
        "icon": "publicicon.png"
    }
    app = model.Application(data)
    assert app.id == "app.public"
    assert app.title == "Public App"
    assert app.icon == "publicicon.png"
    # Make sure string representation contains title
    assert "Public App" in str(app)