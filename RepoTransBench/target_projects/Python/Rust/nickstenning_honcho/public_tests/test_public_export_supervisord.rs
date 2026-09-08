use crate::export::supervisord::*;

#[test]
fn test_get_program_name_public() {
    assert_eq!(get_program_name("supapp", "qwe", 9), "supapp-qwe-9");
    assert_eq!(get_program_name("jazz", "band", 4), "jazz-band-4");
}
#[test]
fn test_get_master_name_public() {
    assert_eq!(get_master_name("testfoo"), "testfoo-master");
    assert_eq!(get_master_name("lemur"), "lemur-master");
}