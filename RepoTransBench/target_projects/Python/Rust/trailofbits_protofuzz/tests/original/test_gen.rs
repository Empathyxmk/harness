use crate::gen;

#[test]
fn test_message_generator_simple() {
    // Dummy for message_generator: yields two DummyMsg1 objects
    #[derive(Default, Clone)]
    struct DummyMsg1;
    fn dummy_valgen(_t: &str, _f: Option<&str>) -> Box<dyn Iterator<Item = i32>> {
        Box::new(vec![1, 2].into_iter())
    }
    let objs: Vec<DummyMsg1> = gen::message_generator::<DummyMsg1, _>(DummyMsg1, dummy_valgen, 2).collect();
    assert_eq!(objs.len(), 2);
}

#[test]
fn test_message_generator_with_message_type() {
    #[derive(Default, Clone)]
    struct AnotherType;
    fn dummy_valgen(_t: &str, _f: Option<&str>) -> Box<dyn Iterator<Item = i32>> {
        Box::new(vec![123].into_iter())
    }
    let objs: Vec<AnotherType> = gen::message_generator::<AnotherType, _>(AnotherType, dummy_valgen, 1).collect();
    assert_eq!(objs.len(), 1);
}

#[test]
fn test__assign_to_field_param() {
    struct DummyObj;
    struct FieldD { label: i32, name: &'static str }
    let mut obj = DummyObj;
    let field = FieldD { label: 1, name: "foo" };
    let value = 42;
    let out = gen::_assign_to_field(&mut obj, &gen::FieldD { label: field.label, name: field.name }, value);
    assert_eq!(out, vec![42]);
}