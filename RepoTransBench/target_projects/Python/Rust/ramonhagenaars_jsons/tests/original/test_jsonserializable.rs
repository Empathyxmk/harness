use crate::jsons;
use serde::{Serialize, Deserialize};

#[derive(Debug, Serialize, Deserialize, PartialEq)]
struct Person {
    name: String,
    age: u32,
}

#[test]
fn test_jsonserializable() {
    let person = Person { name: "John".to_string(), age: 65 };
    let person_json = jsons::dump(&person);
    let person_json_str = jsons::dumps(&person);
    let person_json_bytes = jsons::dumpb(&person);

    let person_loaded: Person = jsons::load(person_json.clone());
    let person_loaded_from_bytes: Person = jsons::loadb(&person_json_bytes);

    let expected_json = serde_json::json!({"name": "John", "age": 65});

    assert_eq!(person_json, expected_json);
    assert_eq!(jsons::dump(&person), expected_json);
    assert_eq!(serde_json::from_str::<serde_json::Value>(&person_json_str).unwrap(), expected_json);
    assert_eq!(
        serde_json::from_slice::<serde_json::Value>(&person_json_bytes).unwrap(),
        expected_json
    );
    assert_eq!(jsons::dump(&person_loaded), expected_json);
    assert_eq!(person_loaded.name, "John");
    assert_eq!(person_loaded.age, 65);
    assert_eq!(person_loaded_from_bytes.name, "John");
    assert_eq!(person_loaded_from_bytes.age, 65);
}

#[derive(Debug, Serialize, Deserialize, PartialEq)]
struct PersonWithCamel {
    my_name: String,
}

#[test]
fn test_jsonserializable_with_kwargs() {
    // In Rust, customize with serde attributes.
    #[derive(Debug, Serialize, Deserialize, PartialEq)]
    struct PersonCamel {
        #[serde(rename = "myName")]
        my_name: String,
    }
    let person = PersonCamel { my_name: "John".to_string() };
    let person_json = jsons::dump(&person);
    assert_eq!(person_json, serde_json::json!({"myName": "John"}));

    let person_loaded: PersonCamel = jsons::load(person_json.clone());
    assert_eq!(person_loaded.my_name, "John");
}

#[test]
fn test_with_load() {
    #[derive(Debug, Serialize, Deserialize, PartialEq)]
    struct Foo {
        bar: u64,
        #[serde(default = "default_ham")]
        ham: String,
    }
    fn default_ham() -> String { "spam".to_string() }

    let json = serde_json::json!({"bar": 42});
    let loaded: Foo = jsons::load(json);
    assert_eq!(loaded.ham, "spam");
    assert_eq!(loaded.bar, 42);
}

// More advanced tests with forking serializers/deserializers like in Python
// are not directly applicable in Rust's serde model.