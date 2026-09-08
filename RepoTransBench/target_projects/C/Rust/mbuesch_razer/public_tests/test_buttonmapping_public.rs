#[test]
fn test_buttonmapping_public() {
    const BUTTON_MAPPING_SIZE: usize = 4;
    struct ButtonMap {
        mapping: [i32; BUTTON_MAPPING_SIZE],
    }

    let mut bm = ButtonMap {
        mapping: [0; BUTTON_MAPPING_SIZE],
    };
    let init_values = [10, 20, 30, 40];
    for i in 0..BUTTON_MAPPING_SIZE {
        bm.mapping[i] = init_values[i];
    }
    for i in 0..BUTTON_MAPPING_SIZE {
        assert_eq!(bm.mapping[i], init_values[i]);
    }
    println!("test_buttonmapping_public passed");
}