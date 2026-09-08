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
    // Use different input set
    if bmp_get_padding(5) == 1 &&
        bmp_get_padding(6) == 2 &&
        bmp_get_padding(9) == 3 &&
        bmp_get_padding(12) == 0 &&
        bmp_get_padding(13) == 1 &&
        bmp_get_padding(14) == 2 &&
        bmp_get_padding(15) == 3 &&
        bmp_get_padding(16) == 0
    {
        print_passed("BMP_GET_PADDING_public");
        1
    } else {
        print_failed("BMP_GET_PADDING_public");
        0
    }
}

// Header

fn bmp_test_header_size() -> i32 {
    if std::mem::size_of::<BmpHeader>() == 12 {
        print_passed("header_size_public");
        1
    } else {
        print_failed("header_size_public");
        0
    }
}

fn bmp_test_header_init_df() -> i32 {
    let mut passed = 1;
    let mut header = BmpHeader::default();
    bmp_header_init_df(&mut header, 77, 55);
    if header.bf_size != (std::mem::size_of::<BmpPixel>() * 77 * 55) as u32 ||
        header.bi_width != 77 ||
        header.bi_height != 55 {
        passed = 0;
    }
    bmp_header_init_df(&mut header, 20, -30);
    if header.bf_size != (std::mem::size_of::<BmpPixel>() * 20 * 30) as u32 + (bmp_get_padding(20) * 30) as u32 ||
         header.bi_width != 20 ||
         header.bi_height != -30 {
        passed = 0;
    }

    if passed == 1 {
        print_passed("header_init_df_public");
        1
    } else {
        print_failed("header_init_df_public");
        0
    }
}

// Pixel

fn bmp_test_pixel_init() -> i32 {
    let mut pxl = BmpPixel::default();
    bmp_pixel_init(&mut pxl, 128, 64, 32);
    if pxl.red == 128 && pxl.green == 64 && pxl.blue == 32 {
        print_passed("pixel_init_public");
        1
    } else {
        print_failed("pixel_init_public");
        0
    }
}

#[test]
fn test_public_basic_suite() {
    println!("LibBMP-Public-Test (Rust Port)");
    let mut points = 0;

    points += bmp_test_get_padding();
    points += bmp_test_header_size();
    points += bmp_test_header_init_df();
    points += bmp_test_pixel_init();

    print_summary(points, 4);
    assert_eq!(points, 4, "Not all public tests passed (see output)");
}