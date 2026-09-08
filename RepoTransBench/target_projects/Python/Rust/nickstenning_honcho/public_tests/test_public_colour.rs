use crate::colour::get_colour;

#[test]
fn test_public_get_colour_values() {
    assert!(get_colour("zebra") >= 0);
    assert!(get_colour("lemon") >= 0);
    assert_eq!(get_colour("zebra"), get_colour("zebra"));
    assert_eq!(get_colour("lemon"), get_colour("lemon"));
    assert_ne!(get_colour("zebra"), get_colour("lemon"));
}