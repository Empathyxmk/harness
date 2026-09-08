use crate::constants;

#[test]
fn test_constants_have_title_and_suffix() {
    assert!(constants::TITLE.len() > 0);
    assert!(constants::WATCHER_SUFFIX.len() > 0);
}