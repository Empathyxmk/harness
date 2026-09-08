use crate::gen;

#[test]
fn test_message_generator_simple_public() {
    #[derive(Default, Clone)]
    struct DummyMsg;
    fn dummy_valgen(_t: &str, _f: Option<&str>) -> Box<dyn Iterator<Item = i32>> {
        Box::new(vec![99, 100].into_iter())
    }
    let objs: Vec<DummyMsg> = gen::message_generator::<DummyMsg, _>(DummyMsg, dummy_valgen, 2).collect();
    assert_eq!(objs.len(), 2);
}

#[test]
fn test_message_generator_with_message_type_public() {
    #[derive(Default, Clone)]
    struct AnotherDummyMessageType;
    fn dummy_valgen(_t: &str, _f: Option<&str>) -> Box<dyn Iterator<Item = i32>> {
        Box::new(vec![321].into_iter())
    }
    let objs: Vec<AnotherDummyMessageType> = gen::message_generator::<AnotherDummyMessageType, _>(AnotherDummyMessageType, dummy_valgen, 1).collect();
    assert_eq!(objs.len(), 1);
}

#[test]
fn test__assign_to_field_public() {
    struct DummyObj;
    struct FieldD { label: i32, name: &'static str }
    let mut obj = DummyObj;
    for label in [1, 2, 3] {
        let field = FieldD { label, name: "bar" };
        let value = 77;
        let out = gen::_assign_to_field(&mut obj, &gen::FieldD { label: field.label, name: field.name }, value);
        assert_eq!(out, vec![77]);
    }
}