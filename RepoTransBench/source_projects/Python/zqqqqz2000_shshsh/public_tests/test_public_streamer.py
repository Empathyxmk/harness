from shshsh.streamer import Streamer

def test_public_streamer_basics():
    s = Streamer()
    # check type and basic attribute
    assert hasattr(s, "pipe_read")
    assert hasattr(s, "pipe_write")