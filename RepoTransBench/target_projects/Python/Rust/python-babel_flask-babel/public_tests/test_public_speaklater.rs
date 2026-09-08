// Minimal Rust translation of public_tests/test_public_speaklater.py

#[derive(Clone)]
struct LazyString {
    func: fn() -> String,
}

impl LazyString {
    fn new(func: fn() -> String) -> Self {
        Self { func }
    }
}

impl std::fmt::Display for LazyString {
    fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
        write!(f, "{}", (self.func)())
    }
}

impl std::ops::Add<&str> for LazyString {
    type Output = String;
    fn add(self, rhs: &str) -> String {
        format!("{}{}", (self.func)(), rhs)
    }
}
impl std::ops::Add<LazyString> for &str {
    type Output = String;
    fn add(self, rhs: LazyString) -> String {
        format!("{}{}", self, (rhs.func)())
    }
}

impl std::cmp::PartialEq<LazyString> for LazyString {
    fn eq(&self, other: &LazyString) -> bool {
        (self.func)() == (other.func)()
    }
}
impl std::cmp::PartialOrd<LazyString> for LazyString {
    fn partial_cmp(&self, other: &Self) -> Option<std::cmp::Ordering> {
        Some((self.func)().cmp(&(other.func)()))
    }
}

#[test]
fn test_public_lazy_string_str_addition() {
    let s = LazyString::new(|| "alpha".to_string());
    assert_eq!(s.clone() + "beta", "alphabeta");
    assert_eq!("BETA:".to_string() + s.clone(), "BETA:alpha");
}

#[test]
fn test_public_lazy_string_repeat() {
    let s = LazyString::new(|| "xy".to_string());
    let three = format!("{}{}{}", s.clone(), s.clone(), s.clone());
    assert_eq!(three, "xyxyxy");
}

#[test]
fn test_public_lazy_string_formatting() {
    let s = LazyString::new(|| "Hello, Haruka!".to_string());
    assert_eq!(format!("{}", s), "Hello, Haruka!");
}

#[test]
fn test_public_lazy_string_html() {
    let s = LazyString::new(|| "<p>Test</p>".to_string());
    assert_eq!(format!("{}", s), "<p>Test</p>");
}

#[test]
fn test_public_lazy_string_comparisons() {
    let s1 = LazyString::new(|| "ten".to_string());
    let s2 = LazyString::new(|| "twenty".to_string());
    assert!(format!("{}", s1.clone()) < format!("{}", s2.clone()));
    assert!(format!("{}", s2) > format!("{}", s1));
}