use flask_babel_rs::*;

#[test]
fn test_basics() {
    let babel = Babel::new();
    let n: f64 = 1099.0;
    assert!(babel.format_decimal(1010.99).starts_with("1010"));
    assert!(babel.format_currency(n, "USD").contains("USD"));
    assert!(babel.format_percent(0.19).contains("%"));
    assert!(babel.format_scientific(10000.0).contains("E"));
}