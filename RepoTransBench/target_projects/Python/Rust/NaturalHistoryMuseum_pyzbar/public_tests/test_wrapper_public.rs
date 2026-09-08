fn get_symbol_name(symbol: i32) -> &'static str {
    match symbol {
        13 => "PDF417", // 13
        _ => "UNKNOWN"
    }
}

#[test]
fn test_get_symbol_name() {
    let name = get_symbol_name(13);
    assert!(name.contains("PDF417"));
}

#[test]
fn test_get_symbol_name_invalid() {
    let name = get_symbol_name(1000);
    assert_eq!(name, "UNKNOWN");
}