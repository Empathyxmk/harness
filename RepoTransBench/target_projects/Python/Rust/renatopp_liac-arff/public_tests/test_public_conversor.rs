// Translation of public_tests/test_public_conversor.py

use liac_arff_rs::arff::{ArffObject, AttributeType, ArffValue, dumps, loads};

#[test]
fn test_to_from_string() {
    let obj = ArffObject {
        description: Some("convert".to_string()),
        relation: "convert_case".to_string(),
        attributes: vec![
            ("temperature".to_string(), AttributeType::Real),
            ("weather".to_string(), AttributeType::Nominal(vec!["sunny".to_string(), "rainy".to_string()])),
        ],
        data: vec![
            vec![ArffValue::Num(23.5), ArffValue::String("sunny".to_string())],
            vec![ArffValue::Num(16.2), ArffValue::String("rainy".to_string())],
        ],
    };
    let s = dumps(&obj);
    let out = loads(&s);
    assert_eq!(out.data, obj.data);
    assert_eq!(out.relation, "convert_case");
}