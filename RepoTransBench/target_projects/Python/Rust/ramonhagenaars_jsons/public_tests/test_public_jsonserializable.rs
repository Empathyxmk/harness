use crate::jsons;
use serde::{Serialize, Deserialize};

#[derive(Debug, Serialize, Deserialize, PartialEq)]
struct Animal {
    species: String,
    age: u32,
}

#[test]
fn test_jsonserializable_dump_public() {
    let a = Animal { species: "cat".to_string(), age: 4 };
    assert_eq!(jsons::dump(&a), serde_json::json!({"species":"cat", "age":4}));
}

#[test]
fn test_jsonserializable_load_public() {
    let json = serde_json::json!({"species": "dog", "age": 10});
    let obj: Animal = jsons::load(json);
    assert_eq!(obj.species, "dog");
    assert_eq!(obj.age, 10);
}