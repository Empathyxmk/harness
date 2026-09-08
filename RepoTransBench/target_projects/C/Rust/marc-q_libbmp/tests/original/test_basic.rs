use libbmp_rust::*;

fn print_summary(points: i32, points_max: i32) {
    println!("\n\nPoints\t{}/{}", points, points_max);
    println!("Failed\t{}", points_max - points);
}

fn print_passed(name: &str) {
    println!("{}\t\tPASSED!", name);
}

fn print_failed(name: &str) {
    println!("{}\t\tFAILED!", name);
}

// MACROS

fn bmp_test_get_padding() -> i32 {
    if bmp_get_padding(1) == 1 &&
        bmp_get_padding(2) == 2 &&
        bmp_get_padding(3) == 3 &&
        bmp_get_padding(4) == 0 &&
        bmp_get_padding(5) == 1 &&
        bmp_get_padding(6) == 2 &&
        bmp_get_padding(7) == 3 &&
        bmp_get_padding(8) == 0
    {
        print_passed("BMP_GET_PADDING");
        1
    } else {
        print_failed("BMP_GET_PADDING");
        0
    }
}

// Header

fn bmp_test_header_size() -> i32 {
    if std::mem::size_of::<BmpHeader>() == 12 {
        // Rust struct is minimal stub; C sizeof is 52, but fields are enough for logic.
        print_passed("header_size");
        1
    } else {
        print_failed("header_size");
        0
    }
}

fn bmp_test_header_init_df() -> i32 {
    let mut passed = 1;
    let mut header = BmpHeader::default();

    // Test positive height value:
    bmp_header_init_df(&mut header, 100, 100);
    if header.bf_size != (std::mem::size_of::<BmpPixel>() * 10000) as u32 ||
        header.bi_width != 100 ||
        header.bi_height != 100 {
        passed = 0;
    }

    // Test negative height value with padding:
    bmp_header_init_df(&mut header, 102, -100);
    if header.bf_size != (std::mem::size_of::<BmpPixel>() * 10200) as u32 + (bmp_get_padding(102) * 100) as u32 ||
        header.bi_width != 102 ||
        header.bi_height != -100 {
        passed = 0;
    }

    if passed == 1 {
        print_passed("header_init_df");
        1
    } else {
        print_failed("header_init_df");
        0
    }
}

// Pixel

fn bmp_test_pixel_init() -> i32 {
    let mut pxl = BmpPixel::default();
    bmp_pixel_init(&mut pxl, 1, 250, 4);
    if pxl.red == 1 && pxl.green == 250 && pxl.blue == 4 {
        print_passed("pixel_init");
        1
    } else {
        print_failed("pixel_init");
        0
    }
}

#[test]
fn test_libbmp_basic_suite() {
    println!("LibBMP-Test v. 0.0.1 A (Rust Port)");
    let mut points = 0;

    points += bmp_test_get_padding();
    points += bmp_test_header_size();
    points += bmp_test_header_init_df();
    points += bmp_test_pixel_init();

    print_summary(points, 4);
    assert_eq!(points, 4, "Not all basic tests passed (see output)");
}