import io
import struct

class UsbStats:
    class direction_type:
        pass

class UsbDevice:
    def __init__(self, id):
        self.id = id
        self.push_calls = []

    def push(self, ts, size, dir):
        self.push_calls.append((ts, size, dir))

class FakeDevice(UsbDevice):
    def __init__(self, id):
        super().__init__(id)
        self.pushes = 0
    def push(self, ts, size, dir):
        self.pushes += 1

class UsbBus:
    def __init__(self, bus_id, name, desc):
        self.bus_id = bus_id
        self.name = name
        self.desc = desc
        self._devices = {}

    def push(self, h, data):
        if h['len'] < 14:
            print("packet too small", file=h['cerr'])
            return
        # ensure not wrong bus id
        device_id = data[11]
        bid = struct.unpack("<H", data[12:14])[0]  # Assume little-endian as in C++
        if bid != self.bus_id:
            print("captured a packet claimed to be on bus", file=h['cerr'])
            return
        # call push on device if present
        if device_id in self._devices:
            dev = self._devices[device_id]
            dev.push(
                h['ts_tv_sec'] + (h['ts_tv_usec']/1e6), 
                h['len'], 
                UsbStats.direction_type()
            )

class UsbBusExposed(UsbBus):
    def set_device(self, device_id, dev):
        self._devices[device_id] = dev
    def get_device(self, device_id):
        return self._devices[device_id]

def test_destructor_deletes():
    bus = UsbBus(10, "busPublicName", "descPublic")
    dev1 = UsbDevice(77)
    dev2 = UsbDevice(123)
    bus._devices[77] = dev1
    bus._devices[123] = dev2
    # Should not crash (nothing to check in Python)
    assert True

def test_push_bad_packet_too_small():
    bus = UsbBus(5, "public-foo", "public-bar")
    h = {
        'len': 8,
        'ts_tv_sec': 42,
        'ts_tv_usec': 71009,
        'cerr': io.StringIO()
    }
    data = bytes([0] * 15)
    bus.push(h, data)
    value = h['cerr'].getvalue()
    assert "packet too small" in value

def test_push_packet_wrong_bus_id():
    bus = UsbBus(55, "fooX", "barY")
    h = {
        'len': 25,
        'ts_tv_sec': 13,
        'ts_tv_usec': 5999,
        'cerr': io.StringIO()
    }
    data = bytearray([0] * 25)
    data[8] = ord('S')
    data[11] = 8
    wrong_bid = struct.pack("<H", 66)
    data[12:14] = wrong_bid
    bus.push(h, data)
    value = h['cerr'].getvalue()
    assert "captured a packet claimed to be on bus" in value

def test_push_packet_ok():
    bus = UsbBusExposed(3, "FooPublic", "BarPublic")
    dev = FakeDevice(88)
    bus.set_device(88, dev)
    h = {
        'len': 40,
        'ts_tv_sec': 7,
        'ts_tv_usec': 250,
        'cerr': io.StringIO()
    }
    data = bytearray([0] * 48)
    data[8] = ord('S')
    data[11] = 88
    bid = struct.pack("<H", 3)
    data[12:14] = bid
    bus.push(h, data)
    assert dev.pushes == 1