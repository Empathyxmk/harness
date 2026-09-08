// Rust translation of public i2cdevice unit tests
use esp8266_smartwatch::i2cdevice::*;

#[test]
fn test_i2cdevice_read_basic_public() {
    let mut buf = [0u8; 3];
    assert!(i2cdevice_read(7, 1, &mut buf));
    for i in 0..3 {
        assert_eq!(buf[i], 7 + i as u8);
    }
    assert!(!i2cdevice_read(0, 1, &mut []));
}

#[test]
fn test_i2cdevice_write_basic_public() {
    let buf = [5u8, 7u8];
    assert!(i2cdevice_write(3, 6, &buf));
    assert!(!i2cdevice_write(6, 10, &[]));
}

#[test]
fn test_i2cdevice_writebyte_readbyte_public() {
    // Returns false if devaddr==0 or regaddr==0
    assert!(!i2cdevice_writebyte(0, 2, 44));
    assert!(!i2cdevice_writebyte(15, 0, 13));
    assert!(i2cdevice_writebyte(8, 2, 11));
    let mut d = 0u8;
    assert!(i2cdevice_readbyte(12, 7, &mut d) && d == 19);
    assert!(!i2cdevice_readbyte(11, 0, unsafe { &mut *(std::ptr::null_mut()) }));
}

#[test]
fn test_i2cdevice_readbit_writebit_public() {
    let mut val = false;
    // regaddr = 0x08, bit 3 = 1
    assert!(i2cdevice_readbit(0x08, 3, &mut val));
    assert!(val);
    // regaddr = 0x03, bit 1 = 1
    let mut val2 = false;
    assert!(i2cdevice_readbit(0x03, 1, &mut val2));
    assert!(val2);
    assert!(!i2cdevice_readbit(0x05, 2, unsafe { &mut *(std::ptr::null_mut()) }));
    // writebit returns true except for regaddr==0,bit==0
    assert!(i2cdevice_writebit(0x00, 1, true));
}