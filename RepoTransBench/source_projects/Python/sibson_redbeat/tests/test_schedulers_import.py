def test_scheduler_imports():
    # Just a smoke test for importing critical classes
    from redbeat.schedulers import RedBeatScheduler, RedBeatSchedulerEntry
    assert RedBeatScheduler is not None
    assert RedBeatSchedulerEntry is not None