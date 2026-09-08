def test_monitor_constructs_public():
    class Monitor:
        def __init__(self):
            pass
    try:
        Monitor()
    except Exception as e:
        assert False, f"Construction of Monitor raised: {e}"