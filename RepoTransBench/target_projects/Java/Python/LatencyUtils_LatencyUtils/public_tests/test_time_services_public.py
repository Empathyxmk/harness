def test_nano_time_and_forward():
    class TimeServices:
        _fake_time = 0
        @classmethod
        def nano_time(cls):
            return cls._fake_time
        @classmethod
        def move_time_forward_msec(cls, msec):
            cls._fake_time += msec * 1_000_000
    start = TimeServices.nano_time()
    TimeServices.move_time_forward_msec(16)
    end = TimeServices.nano_time()
    assert end == start + 16_000_000