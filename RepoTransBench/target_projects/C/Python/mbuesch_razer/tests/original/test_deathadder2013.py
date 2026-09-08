import pytest

# Mocks
class RazerMouseUsbCtx:
    def __init__(self):
        self.h = 1

class RazerMouse:
    def __init__(self):
        self.usb_ctx = None

class Deathadder2013Private:
    def __init__(self, m):
        self.m = m

class Deathadder2013Command:
    def __init__(self):
        # There might be a specific size for the structure in C. We'll simulate 16 bytes.
        self.buf = bytearray(16)
        self.command = 0
        self.request = 0

def razer_error(msg, *args):
    pass

# Simulate control transfer behavior
class ControlTransferMock:
    def __init__(self):
        self.call = 0
    def libusb_control_transfer(self, h, flags, request, command, zero, buf, size, timeout):
        self.call += 1
        if self.call == 1:
            return -1
        return size

def deathadder2013_command_init(cmd):
    cmd.buf = bytearray([0] * len(cmd.buf))
    # In C, all members set to zero (already done above)
    cmd.command = 0
    cmd.request = 0

def deathadder2013_usb_write(priv, a, b, buf, size, control_mock=None):
    if control_mock is None:
        control_mock = ControlTransferMock()
    # First call always fails
    rc = control_mock.libusb_control_transfer(
        priv.m.usb_ctx.h, 0, 0, 0, 0, buf.buf, size, 500
    )
    if rc < 0:
        return -1
    return 0

def test_command_init():
    cmd = Deathadder2013Command()
    # fill with 0xFF
    cmd.buf = bytearray([0xFF] * len(cmd.buf))
    deathadder2013_command_init(cmd)
    assert all(b == 0 for b in cmd.buf)

def test_usb_write_error_and_success():
    ctx = RazerMouseUsbCtx()
    m = RazerMouse()
    m.usb_ctx = ctx
    priv = Deathadder2013Private(m)
    buf = Deathadder2013Command()
    # Mock control transfer so first call fails
    control_mock = ControlTransferMock()
    rc = deathadder2013_usb_write(priv, 1, 2, buf, len(buf.buf), control_mock)
    assert rc == -1
    # In the C test, next call would succeed, but we only test the error-case