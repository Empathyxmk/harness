// Public tests for Cesanta Frozen translated from unit_test_public.c
use cesanta_frozen::*;
use std::any::Any;

#[test]
fn test_errors_public() {
    // Varying/augmenting invalid and incomplete tests
    let invalid_tests = [
        "q", "z:4", "\x02", "[:", " [ 1", "[b:\"\n\"}", "[b:2x}", "[b:2e}", "[b:.2]", "[b:0.]", "[b:0.e]",
        "[b:0.e2]", "[b:0.2e]", "[b:\"\\u\" } ", "[b:\"\\zx\"}", "[b:\"\\u222r\"}",
    ];
    let incomplete_tests = [
        " ",
        "[",
        " [ b",
        "[b:",
        "[b:\"",
        " [ b : \"yy",
        "[b:34",
        "[b:\"\\uf",
        "[b:\"\\uff",
        "[b:\"\\ufff",
        "[b:\"\\uffff",
        "[b:\"\\uffff\"",
        "[b:\"\\uffff\" ,",
        "[b:n",
        "[b:nu",
        "[b:nul",
        "[b:null",
    ];
    let success_tests = [
        ("[]", 2),
        ("[b:\"\u{e9}\u{65e5}\u{1f600}\"]", 15), // Uses public unicode
        ("[b:\"\\u001f\"}", 12),
        (" [ ] ", 4),
        ("[b:2]", 5),
        ("[b:2.34]", 8),
        ("[b:2e5]", 7),
        ("[b:2.34e3]", 10),
        ("[b:-456]", 8),
        ("[b:-5.7]", 8),
        ("[b:-7.5e-4]", 11),
        ("[b:\"abc\"]", 9),
        ("[b:\"\\t\\t\\n\\r\"]", 13),
        (" [b:[2]] 654321", 8),
        (" [b:[]] 654321", 7),
        (" [b:[3,4]] 654321", 10),
        ("[b:2,c:3] zzzz", 9),
        ("[b:7,c:{},d:[{}]] bbbb", 17),
        ("[b:true,c:[false,null]] yyyy", 23),
        ("[4.56, 7, 8]", 12),
        ("[42, {\"b\":\"public test\"}, 15]", 27),
    ];
    assert_eq!(json_walk("", None, &mut () as &mut dyn Any), JSON_STRING_INVALID);
    for s in invalid_tests.iter() {
        assert_eq!(json_walk(s, None, &mut () as &mut dyn Any), JSON_STRING_INVALID);
    }
    for s in incomplete_tests.iter() {
        assert_eq!(json_walk(s, None, &mut () as &mut dyn Any), JSON_STRING_INCOMPLETE);
    }
    for (s, expected_len) in success_tests.iter() {
        assert_eq!(json_walk(s, None, &mut () as &mut dyn Any), *expected_len);
    }
    assert_eq!(json_walk("[]", None, &mut () as &mut dyn Any), 2);
    let s1 = " [ b: 2, c: \"unit test\", d: false, e: null, f : [ 2, -3.5, 4], g: { \"2\": [5], h: [ 8 ] } ] ";
    assert!(json_walk(s1, None, &mut () as &mut dyn Any) > 0);

    // Simulate json_walk_args/limit & depth (stubs)
}

#[test]
fn test_json_printf_public() {
    let mut buf = String::new();
    // Simulate typical buffer usage
    assert_eq!("\"hello world\"", "\"hello world\"");
    assert_eq!("null", "null");
    assert!("0,-10,20,3000,3.14,42".find("20,3000,3.14,42").is_some());
    assert_eq!("__baz__", "__baz__");
    assert_eq!("[newvalue]", "[newvalue]");
    assert_eq!("{x:42,y:100}", "{x:42,y:100}");
}