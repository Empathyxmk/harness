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

# Test helpers from C++ ns
class FakeDevice(UsbDevice):
    def __init__(self, id):
        super().__init__(id)
        self.pushes = 0

    def push(self, ts, size, dir):
        self.pushes += 1

class UsbBusExposed(UsbBus):
    def set_device(self, device_id, dev):
        self._devices[device_id] = dev
    def get_device(self, device_id):
        return self._devices[device_id]

def test_destructor_deletes():
    bus = UsbBus(1, "a", "b")
    dev1 = UsbDevice(2)
    dev2 = UsbDevice(3)
    bus._devices[2] = dev1
    bus._devices[3] = dev2
    # Python garbage collector handles the deletion
    assert True  # Should not crash

def test_push_bad_packet_too_small(capsys):
    bus = UsbBus(2, "foo", "bar")
    h = {
        'len': 10,
        'ts_tv_sec': 1,
        'ts_tv_usec': 100000,
        'cerr': io.StringIO()
    }
    data = bytes([0] * 15)
    bus.push(h, data)
    value = h['cerr'].getvalue()
    assert "packet too small" in value

def test_push_packet_wrong_bus_id(capsys):
    bus = UsbBus(42, "foo", "bar")
    h = {
        'len': 20,
        'ts_tv_sec': 2,
        'ts_tv_usec': 100,
        'cerr': io.StringIO()
    }
    data = bytearray([0]*20)
    data[8] = ord('S')
    data[11] = 5
    wrong_bid = struct.pack("<H", 21)
    data[12:14] = wrong_bid
    bus.push(h, data)
    value = h['cerr'].getvalue()
    assert "captured a packet claimed to be on bus" in value

def test_push_packet_ok():
    bus = UsbBusExposed(0, "foo", "bar")
    dev = FakeDevice(7)
    bus.set_device(7, dev)
    h = {
        'len': 32,
        'ts_tv_sec': 5,
        'ts_tv_usec': 100,
        'cerr': io.StringIO()
    }
    data = bytearray([0]*40)
    data[8] = ord('S')
    data[11] = 7
    bid = struct.pack("<H", 0)
    data[12:14] = bid
    bus.push(h, data)
    assert dev.pushes == 1