import pytest

def test_index_js_import_does_not_throw_public():
    try:
        import src.postal as postal
    except Exception:
        pytest.fail("Importing src.postal (public test) raised an exception unexpectedly.")