import pyzlib

def test_deflate_single_space():
    compressed, *_ = pyzlib.deflate()(data=" ", flush_mode='finish')
    assert compressed is not None

    decompressed = pyzlib.inflate()(compressed, flush_mode='finish')
    assert decompressed == " "

def test_deflate_binary_data():
    bin_data = bytes([2,3,4,5,6])
    compressed, *_ = pyzlib.deflate()(bin_data.decode("latin1"), flush_mode='finish')
    assert compressed is not None

    decomp = pyzlib.inflate()(compressed, flush_mode='finish')
    assert decomp.encode("latin1") == bin_data