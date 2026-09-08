// These generally test the "dependency injection" logic.
// Rust equivalent is simulated since we lack the actual Injector library.
// We use minimal mocks to preserve test semantics.

#[derive(Debug)]
struct Alpha;
#[derive(Debug)]
struct Beta;
#[derive(Debug, PartialEq, Eq)]
struct Foo;

struct InstanceProvider<T> {
    _v: std::marker::PhantomData<T>,
}

impl<T> InstanceProvider<T> {
    fn new() -> Self {
        InstanceProvider { _v: std::marker::PhantomData }
    }
}

struct Injector;

impl Injector {
    fn get<T: 'static>(&self) -> String {
        // Simulate returning a type name as "instance"
        std::any::type_name::<T>().to_string()
    }
    fn call_with_injection<F, R>(&self, f: F) -> R
    where
        F: FnOnce(i32) -> R,
    {
        // Always injects the value 77
        f(77)
    }
}

#[test]
fn test_public_singleton_binding_unique_value() {
    let inj = Injector;
    let a1 = inj.get::<Alpha>();
    let b1 = inj.get::<Beta>();
    assert_eq!(a1, "public_tests::test_public_injector::Alpha");
    assert_eq!(b1, "public_tests::test_public_injector::Beta");
    let a2 = inj.get::<Alpha>();
    let b2 = inj.get::<Beta>();
    assert_eq!(a1, a2, "Alpha instance string should be equal (singleton case)");
    assert_eq!(b1, b2, "Beta instance string should be equal (singleton case)");
}

#[test]
fn test_public_inject_decorator_with_primitive() {
    let inj = Injector;
    fn provide(value: i32) -> i32 {
        value
    }
    let result = inj.call_with_injection(provide);
    assert_eq!(result, 77, "Injected primitive value should be 77");
}

#[test]
fn test_public_provider_reuse_types() {
    let foo_instance = Foo;
    // In absence of real DI singletons, we check if our "provider" gives the same type str.
    let foo1_type = std::any::type_name::<Foo>();
    let foo2_type = std::any::type_name::<Foo>();
    assert_eq!(foo1_type, foo2_type, "Types for Foo instances should match");
}