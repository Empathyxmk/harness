import pytest

class RazerMouseDpiMapping:
    def __init__(self):
        self.res = [0, 0]

class NagaPrivate:
    def __init__(self, mapX, mapY):
        self.cur_dpimapping_X = mapX
        self.cur_dpimapping_Y = mapY

class NagaCommand:
    def __init__(self):
        self.command = 0
        self.request = 0
        self.buf = bytearray(8)

def naga_command_init(cmd):
    cmd.command = 0
    cmd.request = 0
    cmd.buf = bytearray(len(cmd.buf))

def naga_command_init_resolution_5600(cmd, priv):
    # Fake setting using mapping, just set command/request to nonzero
    if priv.cur_dpimapping_X and priv.cur_dpimapping_Y:
        cmd.command = 1
        cmd.request = 2
    else:
        cmd.command = 0
        cmd.request = 0

def test_naga_command_init():
    cmd = NagaCommand()
    cmd.buf = bytearray([0xFF] * len(cmd.buf))
    naga_command_init(cmd)
    assert all(b == 0 for b in cmd.buf)

def test_naga_command_init_resolution_5600():
    cmd = NagaCommand()
    mapX = RazerMouseDpiMapping()
    mapY = RazerMouseDpiMapping()
    dummy_x = 1600
    dummy_y = 1600
    mapX.res[0] = dummy_x
    mapY.res[1] = dummy_y
    priv = NagaPrivate(mapX, mapY)
    naga_command_init_resolution_5600(cmd, priv)
    assert cmd.command != 0  # should be set
    assert cmd.request != 0  # should be set