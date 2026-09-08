#[test]
fn test_buttonmapping() {
    const BUTTON_MAPPING_SIZE: usize = 4;

    struct ButtonMap {
        mapping: [i32; BUTTON_MAPPING_SIZE],
    }

    let mut bm = ButtonMap {
        mapping: [0; BUTTON_MAPPING_SIZE],
    };
    for i in 0..BUTTON_MAPPING_SIZE {
        bm.mapping[i] = i as i32;
    }
    for i in 0..BUTTON_MAPPING_SIZE {
        assert_eq!(bm.mapping[i], i as i32);
    }
    println!("test_buttonmapping passed");
}