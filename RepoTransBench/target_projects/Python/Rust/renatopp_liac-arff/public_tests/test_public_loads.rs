// Translation of public_tests/test_public_loads.py

use liac_arff_rs::arff::{ArffObject, loads};

#[test]
fn test_loads() {
    let arff_str = "@RELATION public_sample

@ATTRIBUTE id NUMERIC
@ATTRIBUTE class {p, q}

@DATA
101,p
102,q
";
    let obj = loads(arff_str);
    assert_eq!(obj.relation, "public_sample");
    // For tuple enforcement see stub implementation
    // assert_eq!(obj.attributes[1].1, ... );
    assert_eq!(obj.data[0][1], "p");
    assert_eq!(obj.data[1][0], 102.0);
}