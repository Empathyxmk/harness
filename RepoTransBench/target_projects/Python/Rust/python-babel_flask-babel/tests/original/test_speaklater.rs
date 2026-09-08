// Translation for tests/test_speaklater.py

#[derive(Clone)]
struct LazyString {
    f: fn() -> String,
}

impl LazyString {
    fn new(f: fn() -> String) -> Self {
        LazyString { f }
    }
}

impl std::fmt::Display for LazyString {
    fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
        let inner = (self.f)();
        write!(f, "{}", inner)
    }
}

impl std::ops::Add<&str> for LazyString {
    type Output = String;
    fn add(self, rhs: &str) -> String {
        format!("{}{}", (self.f)(), rhs)
    }
}

impl std::ops::Add<LazyString> for &str {
    type Output = String;
    fn add(self, rhs: LazyString) -> String {
        format!("{}{}", self, (rhs.f)())
    }
}

#[test]
fn test_str_and_repr() {
    let lz = LazyString::new(|| "value(1,3)".to_string());
    assert_eq!(format!("{}", lz), "value(1,3)");
}

#[test]
fn test_add_radd() {
    let lz = LazyString::new(|| "foo".to_string());
    assert_eq!(lz + "bar", "foobar");
    let lz2 = LazyString::new(|| "foo".to_string());
    assert_eq!("bar".to_string() + lz2, "barfoo");
}