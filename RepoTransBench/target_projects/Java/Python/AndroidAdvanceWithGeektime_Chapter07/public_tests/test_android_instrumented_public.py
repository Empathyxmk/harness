import pytest

class Context:
    def get_package_name(self):
        return "matrix.tencent.com.matrix_android"

def get_app_context():
    return Context()

def test_use_app_context_public():
    app_context = get_app_context()
    assert app_context is not None
    assert app_context.get_package_name() != "com.geektime.systrace.dummy"