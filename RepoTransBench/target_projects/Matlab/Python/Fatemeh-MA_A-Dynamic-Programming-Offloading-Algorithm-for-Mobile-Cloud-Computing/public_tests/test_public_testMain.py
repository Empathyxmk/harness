from src.Main import Main

def test_public_Main():
    executed = False

    def dummy_set_result(*args, **kwargs):
        nonlocal executed
        executed = True

    try:
        Main(set_result=dummy_set_result)
    except Exception as e:
        assert False, f"Main threw an error: {e}"
    assert executed, 'Main script executed without error.'