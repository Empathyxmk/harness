import pytest

class NetUtils:
    DISCONNECTED = 0
    WIFI_CONNECTED = 1
    ETHERNET_CONNECTED = 2

    @staticmethod
    def getNetConnStatus(ctx):
        # ctx will be our mocked context object or None
        if ctx is None:
            return NetUtils.DISCONNECTED

        cm = getattr(ctx, "get_system_service", lambda x: None)("connectivity")
        if cm is None:
            return NetUtils.DISCONNECTED

        wifi_info = cm.get_network_info("wifi")
        if wifi_info and getattr(wifi_info, "is_available", lambda: False)() and getattr(wifi_info, "is_connected", lambda: False)():
            return NetUtils.WIFI_CONNECTED

        eth_info = cm.get_network_info("ethernet")
        if eth_info and getattr(eth_info, "is_available", lambda: False)() and getattr(eth_info, "is_connected", lambda: False)():
            return NetUtils.ETHERNET_CONNECTED

        return NetUtils.DISCONNECTED

    @staticmethod
    def isNetConnected(ctx):
        if ctx is None:
            return False
        cm = getattr(ctx, "get_system_service", lambda x: None)("connectivity")
        if cm is None:
            return False
        infos = cm.get_all_network_info()
        if infos is None:
            return False
        for info in infos:
            if getattr(info, "is_connected", lambda: False)():
                if getattr(info, "get_state", lambda: None)() == "CONNECTED":
                    return True
        return False

    @staticmethod
    def netConnected(ctx):
        class LiveData:
            def __init__(self, val):
                self._val = val
            def get_value(self):
                return self._val
            def __eq__(self, other):
                return self._val == other
        value = NetUtils.isNetConnected(ctx)
        return LiveData(value)

class DummyInfo:
    def __init__(self, connected=False, available=False, state=None):
        self._connected = connected
        self._available = available
        self._state = state

    def is_connected(self):
        return self._connected
    def is_available(self):
        return self._available
    def get_state(self):
        return self._state

class DummyCM:
    def __init__(self, wifi_info=None, eth_info=None, all_infos=None):
        self._wifi_info = wifi_info
        self._eth_info = eth_info
        self._all_infos = all_infos if all_infos is not None else []

    def get_network_info(self, which):
        if which == "wifi":
            return self._wifi_info
        elif which == "ethernet":
            return self._eth_info
        return None

    def get_all_network_info(self):
        return self._all_infos

class DummyContext:
    def __init__(self, cm=None):
        self._cm = cm

    def get_system_service(self, what):
        if what == "connectivity":
            return self._cm
        return None

def test_get_net_conn_status_null_context():
    assert NetUtils.getNetConnStatus(None) == NetUtils.DISCONNECTED

def test_get_net_conn_status_wifi_connected():
    wifi_info = DummyInfo(connected=True, available=True)
    cm = DummyCM(wifi_info=wifi_info)
    ctx = DummyContext(cm=cm)
    assert NetUtils.getNetConnStatus(ctx) == NetUtils.WIFI_CONNECTED

def test_get_net_conn_status_ethernet_connected():
    wifi_info = DummyInfo(connected=False, available=False)
    eth_info = DummyInfo(connected=True, available=True)
    cm = DummyCM(wifi_info=wifi_info, eth_info=eth_info)
    ctx = DummyContext(cm=cm)
    assert NetUtils.getNetConnStatus(ctx) == NetUtils.ETHERNET_CONNECTED

def test_get_net_conn_status_none():
    cm = DummyCM()
    ctx = DummyContext(cm=cm)
    assert NetUtils.getNetConnStatus(ctx) == NetUtils.DISCONNECTED

def test_is_net_connected_null_context():
    assert not NetUtils.isNetConnected(None)

def test_is_net_connected_connected():
    info = DummyInfo(connected=True, state="CONNECTED")
    cm = DummyCM(all_infos=[info])
    ctx = DummyContext(cm=cm)
    assert NetUtils.isNetConnected(ctx)

def test_is_net_connected_none():
    cm = DummyCM(all_infos=None)
    ctx = DummyContext(cm=cm)
    assert not NetUtils.isNetConnected(ctx)

def test_is_net_connected_not_connected():
    info = DummyInfo(connected=False)
    cm = DummyCM(all_infos=[info])
    ctx = DummyContext(cm=cm)
    assert not NetUtils.isNetConnected(ctx)

def test_net_connected_null_context():
    live = NetUtils.netConnected(None)
    assert live is not None
    assert live.get_value() is False