use serde::{Serialize, Deserialize};
use chrono::NaiveDate;
use std::collections::HashMap;

#[cfg(test)]
mod tests {
    use super::*;
    use uuid::Uuid;
    use std::str::FromStr;
    use rust_decimal::Decimal;

    #[derive(Debug, Clone, PartialEq, Serialize, Deserialize)]
    struct Person {
        name: String,
        length: i32,
        birth_date: Option<NaiveDate>,
    }

    #[derive(Debug, Clone, PartialEq, Serialize, Deserialize)]
    struct Group {
        leader: Person,
        people: Vec<Person>,
    }

    // -- test_many
    #[test]
    fn test_many_public() {
        let v = vec![
            Person { name: "Eve".to_string(), length: 3, birth_date: None }
        ];
        let json = serde_json::to_string(&v).unwrap();
        let v2: Vec<Person> = serde_json::from_str(&json).unwrap();
        assert_eq!(v, v2);

        let v_empty: Vec<Person> = vec![];
        let json_empty = serde_json::to_string(&v_empty).unwrap();
        let v2_empty: Vec<Person> = serde_json::from_str(&json_empty).unwrap();
        assert_eq!(v_empty, v2_empty);
    }

    // -- test_definition (Field/properties are present)
    #[test]
    fn test_definition_public() {
        let p = Person {
            name: "Eve".into(),
            length: 456,
            birth_date: None,
        };
        assert_eq!(p.name, "Eve");
        assert_eq!(p.length, 456);
    }

    // -- test_strip_empty (simulate: treat None as absent)
    #[test]
    fn test_strip_empty_public() {
        let in_data = Person {
            name: "Eve".into(),
            length: 456,
            birth_date: None
        };
        let json = serde_json::to_string(&in_data).unwrap();
        let p2: Person = serde_json::from_str(&json).unwrap();
        assert_eq!(in_data, p2);

        let grp = Group {
            leader: in_data.clone(),
            people: vec![
                Person { name: "Mallory".into(), length: 789, birth_date: None }
            ]
        };
        let json = serde_json::to_string(&grp).unwrap();
        let g2: Group = serde_json::from_str(&json).unwrap();
        assert_eq!(grp, g2);
    }

    // -- test_save (simulates: "create" then update/replace/serialize)
    #[test]
    fn test_save_public() {
        let mut inst = Person {
            name: "Eve".to_string(),
            length: 456,
            birth_date: None,
        };
        let json = serde_json::to_string(&inst).unwrap();
        let mut out: Person = serde_json::from_str(&json).unwrap();
        assert_eq!(inst, out);

        // replace length
        out.length = 654;
        assert_eq!(out.length, 654);
        let json = serde_json::to_string(&out).unwrap();
        let p2: Person = serde_json::from_str(&json).unwrap();
        assert_eq!(out, p2);
    }

    #[test]
    fn test_nested_save_public() {
        #[derive(Debug, Clone, PartialEq, Serialize, Deserialize)]
        struct Child { value: String }
        let c = Child { value: "D".into() };
        let json = serde_json::to_string(&c).unwrap();
        let c2: Child = serde_json::from_str(&json).unwrap();
        assert_eq!(c, c2);

        #[derive(Debug, Clone, PartialEq, Serialize, Deserialize)]
        struct Parent { field: Child }
        let parent = Parent { field: c.clone() };
        let json = serde_json::to_string(&parent).unwrap();
        let parent2: Parent = serde_json::from_str(&json).unwrap();
        assert_eq!(parent, parent2);

        #[derive(Debug, Clone, PartialEq, Serialize, Deserialize)]
        struct Grandparent { field: Parent }
        let grandparent = Grandparent { field: parent.clone() };
        let json = serde_json::to_string(&grandparent).unwrap();
        let grandparent2: Grandparent = serde_json::from_str(&json).unwrap();
        assert_eq!(grandparent, grandparent2);

        #[derive(Debug, Clone, PartialEq, Serialize, Deserialize)]
        struct ParentList { fields: Vec<Child> }
        let list = ParentList { fields: vec![
            Child { value: "X".into() }, Child { value: "Y".into() }
        ]};
        let json = serde_json::to_string(&list).unwrap();
        let l2: ParentList = serde_json::from_str(&json).unwrap();
        assert_eq!(list, l2);
    }
}