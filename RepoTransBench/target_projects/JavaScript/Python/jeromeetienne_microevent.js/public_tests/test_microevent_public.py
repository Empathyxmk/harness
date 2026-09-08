# ...[other code stays the same]...
def test_unbind_from_never_bound_event_alternate_public():
    obj = createObj()
    try:
        obj.unbind('not-there', lambda *args: None)
    except Exception as e:
        pytest.fail(f"Unbind on never-bound event should not throw but threw: {e}")
# ...[all other handlers, make sure they accept *args if passed values in trigger]...