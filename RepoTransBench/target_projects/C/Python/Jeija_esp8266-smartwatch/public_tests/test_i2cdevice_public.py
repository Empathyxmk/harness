import pytest

# Using the same logic as original, but with different inputs per the C "public" test

def i2cdevice_read(dev_addr, reg_addr, buf):
    if buf is None:
        return False
    n = len(buf)
    for i in range(n):
        buf[i] = dev_addr + i
    if dev_addr == 0 and reg_addr == 1:
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
    return True

def test_i2cdevice_read_basic_public():
    buf = [0]*3
    assert i2cdevice_read(7, 1, buf)
    for i in range(3):
        assert buf[i] == 7+i

    assert not i2cdevice_read(0, 1, None)

def test_i2cdevice_write_basic_public():
    buf = [5, 7]
    assert i2cdevice_write(3, 6, buf)
    assert not i2cdevice_write(6, 10, None)

def test_i2cdevice_writebyte_readbyte_public():
    d = [0]
    assert not i2cdevice_writebyte(0,2,44)
    assert not i2cdevice_writebyte(15,0,13)
    assert i2cdevice_writebyte(8,2,11)
    d2 = [0]
    assert i2cdevice_readbyte(12,7,d2) and d2[0]==19
    assert not i2cdevice_readbyte(11,0,None)

def test_i2cdevice_readbit_writebit_public():
    val = [False]
    assert i2cdevice_readbit(0x08, 3, val)
    assert val[0]
    assert i2cdevice_readbit(0x03, 1, val)
    assert val[0]
    assert not i2cdevice_readbit(0x05, 2, None)
    assert i2cdevice_writebit(0x00,1,True)