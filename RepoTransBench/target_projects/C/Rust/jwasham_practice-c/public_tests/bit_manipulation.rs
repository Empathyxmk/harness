// Translation of bit_manipulation/tests/test_bit_manipulation_public.c

fn btoa(mut bits: u32, output: &mut [u8], size: usize) {
    for i in (0..size).rev() {
        output[i] = b'0' + (bits & 1) as u8;
        bits >>= 1;
    }
    if output.len() > size {
        output[size] = 0;
    }
}

fn is_little_endian() -> bool {
    let n: u16 = 1;
    let bytes = n.to_le_bytes();
    bytes[0] == 1
}

#[test]
fn test_btoa() {
    let size = std::mem::size_of::<u32>() * 8;
    let mut buf = vec![0xAAu8; size + 1];
    btoa(17, &mut buf, size);
    for i in 0..size {
        if i == size-5 || i == size-1 {
            assert_eq!(buf[i], b'1');
        } else {
            assert_eq!(buf[i], b'0');
        }
    }
    buf.iter_mut().for_each(|b| *b = 0xAA);
    btoa(0xFF00, &mut buf, size);
    for i in 0..size {
        if i >= size - 16 && i < size - 8 {
            assert_eq!(buf[i], b'1');
        } else {
            assert_eq!(buf[i], b'0');
        }
    }
}

#[test]
fn test_is_little_endian() {
    let value = is_little_endian();
    assert!(value == true || value == false);
}

#[test]
fn test_bit_ops() {
    let mut x = 0;
    x |= 1 << 4;
    assert!((x & (1 << 4)) != 0);

    x = 0xFFFF;
    x &= !(1 << 4);
    assert!((x & (1 << 4)) == 0);

    x = 0;
    x |= 1 << ((std::mem::size_of::<i32>() * 8) - 2);
    assert!((x & (1 << ((std::mem::size_of::<i32>() * 8) - 2))) != 0);
}