import pytest

# Public version of the CompileConstantsSanity test, with checks for < 1000
try:
    from common import VST_BRIDGE_CMD_PING, VST_BRIDGE_CMD_VERSION, VST_BRIDGE_CMD_INFO
    from common import VST_BRIDGE_RSP_VERSION, VST_BRIDGE_RSP_INFO
    HAS_SYMBOLS = True
except ImportError:
    VST_BRIDGE_CMD_PING = None
    VST_BRIDGE_CMD_VERSION = None
    VST_BRIDGE_CMD_INFO = None
    VST_BRIDGE_RSP_VERSION = None
    VST_BRIDGE_RSP_INFO = None
    HAS_SYMBOLS = False

def test_commonheader_public_compileconstantsboundaries():
    """
    Public version: test that enums/constants are less than 1000, if defined.
    """
    if VST_BRIDGE_CMD_PING is not None:
        ping = VST_BRIDGE_CMD_PING
        assert ping < 1000
    if VST_BRIDGE_CMD_VERSION is not None:
        ver = VST_BRIDGE_CMD_VERSION
        assert ver < 1000
    if VST_BRIDGE_CMD_INFO is not None:
        info = VST_BRIDGE_CMD_INFO
        assert info < 1000
    if VST_BRIDGE_RSP_VERSION is not None:
        rver = VST_BRIDGE_RSP_VERSION
        assert rver < 1000
    if VST_BRIDGE_RSP_INFO is not None:
        rinfo = VST_BRIDGE_RSP_INFO
        assert rinfo < 1000
    assert True  # Succeed always if no constants present (matches SUCCEED())