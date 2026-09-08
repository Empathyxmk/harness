def test_imports():
    # This just checks that the __init__ module imports do not error
    import redbeat
    assert hasattr(redbeat, "RedBeatScheduler")
    assert hasattr(redbeat, "RedBeatSchedulerEntry")