use crate::runner::sensei::*;

#[test]
fn test_public_Sensei_class_exists() {
    // Ensure struct Sensei with new() exists and is callable
    struct DummyDecorator;
    let _s: Sensei<DummyDecorator> = Sensei::new(DummyDecorator);
}
#[test]
fn test_public_Sensei_instance() {
    struct DummyDecorator;
    let s = Sensei::new(DummyDecorator);
    // Ensure s has a type and is a Sensei
    let _class = std::any::type_name_of_val(&s);
}