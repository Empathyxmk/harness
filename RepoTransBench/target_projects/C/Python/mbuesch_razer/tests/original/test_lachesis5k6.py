import pytest

class DummyUsbCtx:
    def __init__(self):
        self.h = 1

class DummyUsbDev:
    pass

class RazerMouse:
    def __init__(self):
        self.usb_ctx = None
        self.idstr = ""

# Global to simulate failure path
razer_synapse_should_fail = {"value": False}

def razer_synapse_init(mouse, unused, feat):
    if razer_synapse_should_fail["value"]:
        return -1
    return 0

def razer_synapse_exit(mouse):
    pass

def razer_synapse_get_serial(mouse):
    return "SERIAL"

def razer_generic_usb_gen_idstr(usbdev, handle, string, flag, serial, idstrbuf):
    return f"FakeID:{string}:{serial}"

def razer_lachesis5k6_init(mouse, dev):
    res = razer_synapse_init(mouse, None, 0)
    if res != 0:
        mouse.idstr = ""
        return -1
    serial = razer_synapse_get_serial(mouse)
    mouse.idstr = razer_generic_usb_gen_idstr(dev, mouse.usb_ctx.h, "Lachesis 5600 DPI", 0, serial, "")
    return 0

def razer_lachesis5k6_release(mouse):
    # Should not crash or hang; no operation in test
    pass

def test_razer_lachesis5k6_init_ok():
    m = RazerMouse()
    m.usb_ctx = DummyUsbCtx()
    m.idstr = ""
    razer_synapse_should_fail["value"] = False
    dev = DummyUsbDev()
    res = razer_lachesis5k6_init(m, dev)
    assert res == 0
    assert "FakeID:Lachesis 5600 DPI:SERIAL" in m.idstr

def test_razer_lachesis5k6_init_fail():
    m = RazerMouse()
    m.usb_ctx = DummyUsbCtx()
    m.idstr = ""
    razer_synapse_should_fail["value"] = True
    dev = DummyUsbDev()
    res = razer_lachesis5k6_init(m, dev)
    assert res != 0
    assert m.idstr == ""

def test_razer_lachesis5k6_release():
    m = RazerMouse()
    # Should not crash/hang
    razer_lachesis5k6_release(m)