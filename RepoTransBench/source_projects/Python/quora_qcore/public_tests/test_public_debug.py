from qcore.debug import print_stack, frame, list_frames
from qcore.asserts import assert_is_not, assert_is_instance

def test_public_print_stack_and_frames_do_not_fail():
    # The main purpose is that these don't raise exceptions
    print_stack()
    f = frame()
    assert_is_instance(f, type(frame()))
    fs = list_frames()
    assert_is_instance(fs, list)
    assert_is_not(fs, None)