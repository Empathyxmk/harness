// Public additional test cases for librope - ported from C test/test_rope_additional_public.c

use librope::{Rope, RopeResult::*};

#[test]
fn test_rope_basic_public() {
    let mut r = Rope::new();
    assert_eq!(r.insert(0, "See you!".as_bytes()), Ok);
    assert_eq!(r.char_count(), 8);
    assert_eq!(r.insert(8, " 🚀".as_bytes()), Ok);
    assert_eq!(r.char_count(), 10);
    assert_eq!(r.insert(4, "Public ".as_bytes()), Ok);

    let contents = r.create_cstr();
    let s = std::str::from_utf8(&contents[..contents.len() - 1]).unwrap();
    assert_eq!(s, "See Public you! 🚀");

    // Delete ' Public y'
    // After the above, string is "See Public you! 🚀"
    // Delete from char index 3, 8 chars: removes positions 3..10 inclusive.
    r.del(3, 8);

    let after_del = r.create_cstr();
    let after = std::str::from_utf8(&after_del[..after_del.len() - 1]).unwrap();
    assert_eq!(after, "Seeyou! 🚀");
}

#[test]
fn test_rope_new_with_utf8_public() {
    let r = Rope::new_with_utf8("💡Fun!".as_bytes()).unwrap();
    assert_eq!(r.char_count(), 5);
    let s = r.create_cstr();
    let c = std::str::from_utf8(&s[..s.len() - 1]).unwrap();
    assert_eq!(c, "💡Fun!");
}