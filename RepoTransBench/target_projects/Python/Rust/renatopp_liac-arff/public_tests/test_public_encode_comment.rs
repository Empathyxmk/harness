// Translation of public_tests/test_public_encode_comment.py

use liac_arff_rs::arff::{ArffObject, AttributeType, ArffValue, dumps};

#[test]
fn test_encode_comment() {
    let obj = ArffObject {
        description: Some("This is a public comment".to_string()),
        relation: "comments_case".to_string(),
        attributes: vec![
            ("id".to_string(), AttributeType::Numeric),
            ("label".to_string(), AttributeType::Nominal(vec!["A".to_string(), "B".to_string()])),
        ],
        data: vec![
            vec![ArffValue::Num(1.0), ArffValue::String("A".to_string())],
            vec![ArffValue::Num(2.0), ArffValue::String("B".to_string())],
        ],
    };
    let s = dumps(&obj);

    assert!(s.contains("This is a public comment"));
    assert!(s.contains("@RELATION comments_case"));
    assert!(s.contains("@ATTRIBUTE id NUMERIC"));
    assert!(s.contains("@ATTRIBUTE label {A, B}"));
}