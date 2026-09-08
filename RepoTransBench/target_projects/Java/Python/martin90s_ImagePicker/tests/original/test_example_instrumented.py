import pytest

class DummyContext:
    def get_package_name(self):
        return "com.imnjh.imagepicker"

def test_use_app_context():
    app_context = DummyContext()
    assert app_context.get_package_name() == "com.imnjh.imagepicker"