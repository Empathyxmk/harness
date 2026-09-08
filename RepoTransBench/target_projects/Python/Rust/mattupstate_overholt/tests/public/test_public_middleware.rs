// Translation of public_tests/test_public_middleware.py

use mattupstate_overholt::middleware;

#[test]
fn test_public_middleware_module_exists() {
    // Always true, but shows presence by compiling.
    let module = std::any::type_name::<middleware::DummyApp>();
    assert!(!module.is_empty());
}