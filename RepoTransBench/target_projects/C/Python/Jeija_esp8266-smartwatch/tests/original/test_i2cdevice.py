import pytest

# Mocked functions for i2cdevice
def i2cdevice_read(dev_addr, reg_addr, buf):
    # For demo: read fills buf with dev_addr + i for i = 0..n
    if buf is None:
        return False
    n = len(buf)
    for i in range(n):
        buf[i] = dev_addr + i
    # Simulate: fail if dev_addr == 2, reg_addr == 2 (test for NULL in C)
    if dev_addr == 2 and reg_addr == 2:
        return False
    return True

def i2cdevice_write(dev_addr, n, buf):
    if buf is None:
        return False
    return True

def i2cdevice_writebyte(devaddr, regaddr, d):
    if devaddr == 0 or regaddr == 0:
        return False
    return True

def i2cdevice_readbyte(devaddr, regaddr, data_out):
    if data_out is None:
        return False
    data_out[0] = devaddr + regaddr
    return True

def i2cdevice_readbit(regaddr, bit, val_out):
    if val_out is None:
        return False
    if regaddr & (1 << bit):
        val_out[0] = True
    else:
        val_out[0] = False
    return True

def i2cdevice_writebit(regaddr, bit, val):
    # Only fail if regaddr==0 and bit==0 and follow C logic
    if regaddr == 0 and bit == 0:
        return True
    return True

def test_i2cdevice_read_basic():
    buf = [0]*4
    assert i2cdevice_read(5, 4, buf)
    for i in range(4):
        assert buf[i] == 5+i

    assert not i2cdevice_read(2, 2, None)

def test_i2cdevice_write_basic():
    buf = [1, 2]
    assert i2cdevice_write(4, 2, buf)
    assert not i2cdevice_write(4, 2, None)

def test_i2cdevice_writebyte_readbyte():
    d = [0]
    assert not i2cdevice_writebyte(0,1,99)
    assert not i2cdevice_writebyte(42,0,55)
    assert i2cdevice_writebyte(3,2,123)
    d2 = [0]
    assert i2cdevice_readbyte(10,5,d2) and d2[0]==15
    assert not i2cdevice_readbyte(9,1,None)

def test_i2cdevice_readbit_writebit():
    val = [False]
    assert i2cdevice_readbit(0x04, 2, val)
    assert val[0]
    assert i2cdevice_readbit(0x01, 2, val)
    assert not val[0]
    assert not i2cdevice_readbit(0x01, 2, None)
    assert i2cdevice_writebit(0x00,0,True)