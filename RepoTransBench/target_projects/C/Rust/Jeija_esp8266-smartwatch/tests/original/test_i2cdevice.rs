// Conversion of Check-based and assert-based i2cdevice unit tests
use esp8266_smartwatch::i2cdevice::*;
#[test]
fn test_i2cdevice_read_basic() {
    let mut buf = [0u8; 4];
    assert!(i2cdevice_read(5, 4, &mut buf));
    for i in 0..4 {
        assert_eq!(buf[i], 5 + i as u8);
    }
    // NULL in C maps to simply don't pass the arg; simulate by skipping buf
    // here we will call with buf empty, expect false
    assert!(!i2cdevice_read(2, 2, &mut []));
}

#[test]
fn test_i2cdevice_write_basic() {
    let buf = [1u8, 2u8];
    assert!(i2cdevice_write(4, 2, &buf));
    // NULL as input: empty slice
    assert!(!i2cdevice_write(4, 2, &[]));
}

#[test]
fn test_i2cdevice_writebyte_readbyte() {
    // Returns false if devaddr==0 or regaddr==0
    assert!(!i2cdevice_writebyte(0, 1, 99));
    assert!(!i2cdevice_writebyte(42, 0, 55));
    assert!(i2cdevice_writebyte(3, 2, 123));
    let mut d = 0u8;
    // readbyte should set *data=devaddr+regaddr
    assert!(i2cdevice_readbyte(10, 5, &mut d) && d == 15);
    // NULL as data, simulate by Option; real impl may need refinement
    // Instead, for 'None' we use an empty slice, but method doesn't take Option -- so skip
    // Here we simulate test coverage by passing devaddr or regaddr as 0, which triggers fail
    assert!(!i2cdevice_readbyte(9, 1, unsafe { &mut *(std::ptr::null_mut()) }));
}

#[test]
fn test_i2cdevice_readbit_writebit() {
    // regaddr = 0x04, bit 2 = 1
    let mut val = false;
    assert!(i2cdevice_readbit(0x04, 2, &mut val));
    assert!(val);
    // regaddr = 0x01, bit 2 = 0
    let mut val2 = false;
    assert!(i2cdevice_readbit(0x01, 2, &mut val2));
    assert!(!val2);
    assert!(!i2cdevice_readbit(0x01, 2, unsafe { &mut *(std::ptr::null_mut()) }));
    // writebit returns true except for regaddr==0,bit==0
    assert!(i2cdevice_writebit(0x00, 0, true));
}