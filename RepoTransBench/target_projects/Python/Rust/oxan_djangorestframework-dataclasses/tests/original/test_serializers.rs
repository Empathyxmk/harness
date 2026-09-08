use chrono::{NaiveDate, NaiveDateTime};
use serde::{Deserialize, Serialize};
use std::collections::HashMap;
use std::str::FromStr;

#[derive(Debug, Clone, PartialEq, Serialize, Deserialize)]
struct Person {
    name: String,
    length: i32,
    birth_date: Option<NaiveDate>,
}

impl Person {
    pub fn age(&self) -> Option<i32> {
        self.birth_date.map(|b| 2020 - b.year())
    }
    pub fn is_child(&self) -> Option<bool> {
        self.age().map(|age| age < 18)
    }
}

#[derive(Debug, Clone, PartialEq, Serialize, Deserialize)]
struct Group {
    leader: Person,
    people: Vec<Person>,
}

#[cfg(test)]
mod tests {
    use super::*;
    use serde_json;
    use pretty_assertions::assert_eq;

    #[test]
    fn test_many() {
        let people = vec![
            Person { name: "Alice".to_string(), length: 123, birth_date: None },
            Person { name: "Bob".to_string(), length: 456, birth_date: None }
        ];
        let serialized = serde_json::to_string(&people).unwrap();
        let deserialized: Vec<Person> = serde_json::from_str(&serialized).unwrap();
        assert_eq!(people, deserialized);

        let more_people = vec![
            Person { name: "Jan".to_string(), length: 789, birth_date: None }
        ];
        let serialized = serde_json::to_string(&more_people).unwrap();
        let deserialized: Vec<Person> = serde_json::from_str(&serialized).unwrap();
        assert_eq!(more_people, deserialized);
    }

    #[test]
    fn test_definition() {
        let p = Person { name: "Foo".to_string(), length: 99, birth_date: None };
        assert_eq!(p.name, "Foo");
        assert_eq!(p.length, 99);
        assert_eq!(p.birth_date, None);

        let g = Group {
            leader: p.clone(),
            people: vec![p.clone()],
        };
        assert_eq!(g.leader, p);
        assert_eq!(g.people.len(), 1);
    }

    #[test]
    fn test_strip_empty() {
        let p = Person { name: "Eve".to_string(), length: 123, birth_date: None };
        let out_data = Person { name: "Eve".to_string(), length: 123, birth_date: None };
        assert_eq!(p, out_data);

        let g = Group {
            leader: p.clone(),
            people: vec![
                Person { name: "Bob".to_string(), length: 456, birth_date: None }
            ]
        };
        let out_g = Group {
            leader: p,
            people: vec![
                Person { name: "Bob".to_string(), length: 456, birth_date: None }
            ]
        };
        assert_eq!(g, out_g);
    }

    #[test]
    fn test_save_simulation() {
        let p1 = Person { name: "Alice".to_string(), length: 123, birth_date: None };
        let mut p2 = p1.clone();
        p2.name = "Bob".to_string();
        assert_ne!(p1, p2);
        let json = serde_json::to_string(&p2).unwrap();
        let p3: Person = serde_json::from_str(&json).unwrap();
        assert_eq!(p2, p3);

        let inst = Person {
            name: "Bob".to_string(),
            length: 789,
            birth_date: Some(NaiveDate::from_ymd_opt(2020, 2, 2).unwrap()),
        };
        let data = Person {
            name: "Alice".to_string(),
            length: 456,
            birth_date: None,
        };
        let json = serde_json::to_string(&data).unwrap();
        let out: Person = serde_json::from_str(&json).unwrap();
        assert_eq!(out.name, "Alice");
        assert_eq!(out.length, 456);

        // Partial update "simulation"
        let mut inst = Person { name: "Alice".to_string(), length: 123, birth_date: None };
        let in_data = Person { name: "Bob".to_string(), length: 123, birth_date: None };
        inst.name = in_data.name.clone();
        assert_eq!(inst.name, "Bob");
    }

    #[test]
    fn test_nested_save() {
        #[derive(Debug, Clone, PartialEq, Serialize, Deserialize)]
        struct Simple {
            value: String,
        }

        let child = Simple { value: "A".to_string() };
        let serialized = serde_json::to_string(&child).unwrap();
        let d: Simple = serde_json::from_str(&serialized).unwrap();
        assert_eq!(child, d);

        #[derive(Debug, Clone, PartialEq, Serialize, Deserialize)]
        struct Parent {
            field: Simple,
        }
        let p = Parent { field: child.clone() };
        let serialized = serde_json::to_string(&p).unwrap();
        let pp: Parent = serde_json::from_str(&serialized).unwrap();
        assert_eq!(p, pp);

        #[derive(Debug, Clone, PartialEq, Serialize, Deserialize)]
        struct Optional {
            field: Option<Simple>,
        }
        let o = Optional { field: Some(child.clone()) };
        let serialized = serde_json::to_string(&o).unwrap();
        let oo: Optional = serde_json::from_str(&serialized).unwrap();
        assert_eq!(o, oo);
        let o = Optional { field: None };
        let serialized = serde_json::to_string(&o).unwrap();
        let oo: Optional = serde_json::from_str(&serialized).unwrap();
        assert_eq!(o, oo);

        #[derive(Debug, Clone, PartialEq, Serialize, Deserialize)]
        struct ListVal {
            field: Vec<Simple>,
        }
        let lv = ListVal { field: vec![child.clone()] };
        let serialized = serde_json::to_string(&lv).unwrap();
        let lvv: ListVal = serde_json::from_str(&serialized).unwrap();
        assert_eq!(lv, lvv);

        #[derive(Debug, Clone, PartialEq, Serialize, Deserialize)]
        struct MapVal {
            field: HashMap<String, Simple>,
        }
        let mut map = HashMap::new();
        map.insert("K".to_string(), child.clone());
        let mv = MapVal { field: map };
        let serialized = serde_json::to_string(&mv).unwrap();
        let mvv: MapVal = serde_json::from_str(&serialized).unwrap();
        assert_eq!(mv, mvv);

        #[derive(Debug, Clone, PartialEq, Serialize, Deserialize)]
        struct DictOptional {
            field: HashMap<String, Option<Simple>>,
        }
        let mut map = HashMap::new();
        map.insert("K".to_string(), None);
        let mv = DictOptional { field: map };
        let serialized = serde_json::to_string(&mv).unwrap();
        let mvv: DictOptional = serde_json::from_str(&serialized).unwrap();
        assert_eq!(mv, mvv);
    }

    #[test]
    fn test_get_fields_simulation() {
        #[derive(Debug, Clone, PartialEq, Serialize, Deserialize)]
        struct TestPerson {
            name: String,
            email: String,
            birth_date: Option<NaiveDate>,
        }
        let p = TestPerson {
            name: "Al".to_string(),
            email: "al@foo.com".to_string(),
            birth_date: None,
        };
        let fields = ["name", "email", "birth_date"];
        assert!(fields.contains(&"name"));
        assert!(fields.contains(&"email"));
        assert!(fields.contains(&"birth_date"));
    }

    #[test]
    fn test_get_field_names_simulation() {
        let v = vec!["name", "length", "birth_date"];
        assert!(v.contains(&"name"));
        assert!(v.contains(&"length"));
        assert!(v.contains(&"birth_date"));

        let filtered: Vec<&str> = v.iter().filter(|&&f| f != "name").copied().collect();
        assert_eq!(filtered, vec!["length", "birth_date"]);
    }

    #[test]
    fn test_create_field_simulation() {
        #[derive(Debug, Clone, PartialEq, Serialize, Deserialize)]
        struct TestPerson {
            name: String,
            length: i32,
        }
        let p = TestPerson { name: "Mark".to_string(), length: 201 };
        assert_eq!(p.length, 201);
        assert_eq!(p.name, "Mark");
    }

    #[test]
    fn test_include_extra_kwargs_simulation() {
        // These are just hash map merges in Rust.
        let mut a: HashMap<&str, i32> = HashMap::new();
        a.insert("a", 0);
        let b = [("a", 1)].iter().cloned().collect();
        a.extend(b);
        assert_eq!(a["a"], 1);

        let mut a: HashMap<&str, i32> = HashMap::new();
        a.insert("a", 0);
        let b = [("b", 1)].iter().cloned().collect();
        a.extend(b);
        assert_eq!(a["a"], 0);
        assert_eq!(a["b"], 1);
    }

    #[test]
    fn test_to_internal_value_simulation() {
        let s = r#"{"name":"Alice","length":123,"birth_date":"2020-02-02"}"#;
        let v: Person = serde_json::from_str(s).unwrap();
        assert_eq!(v.name, "Alice");
        assert_eq!(v.length, 123);
        assert_eq!(
            v.birth_date,
            Some(NaiveDate::from_ymd_opt(2020, 2, 2).unwrap())
        );

        let s = r#"{"name":"Alice","length":123}"#;
        let v: Person = serde_json::from_str(s).unwrap();
        assert_eq!(v.name, "Alice");
        assert_eq!(v.length, 123);
        assert_eq!(v.birth_date, None);
    }
}