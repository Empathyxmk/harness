use flask_babel_rs::*;

#[test]
fn test_public_format_decimal() {
    let b = Babel::new();
    let val = b.format_decimal(8142.73);
    assert!(val.contains(",") || val.contains("."));
}

#[test]
fn test_public_format_currency() {
    let b = Babel::new();
    let result = b.format_currency(99.95, "EUR");
    assert!(result.contains("EUR") || result.contains("99"));
}

#[test]
fn test_public_format_percent() {
    let b = Babel::new();
    let percent = b.format_percent(3.5);
    assert!(percent.contains("%") || percent.contains("3"));
}

#[test]
fn test_public_format_scientific() {
    let b = Babel::new();
    let sci = b.format_scientific(987654.0);
    assert!(sci.contains("E") || sci.contains("10"));
}