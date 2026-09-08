def test_create_flag_different_input():
    class Message:
        def __init__(self):
            self.flags = set()

    def add_flags(msg, flags):
        msg.flags.update(flags)

    flags = set(['DRAFT'])
    msg = Message()
    add_flags(msg, flags)
    assert 'DRAFT' in msg.flags