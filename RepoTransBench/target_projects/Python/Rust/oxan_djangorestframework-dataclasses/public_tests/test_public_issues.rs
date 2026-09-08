use serde::{Serialize, Deserialize};

#[cfg(test)]
mod tests {
    use super::*;
    use serde_json;

    #[derive(Debug, Clone, PartialEq, Serialize, Deserialize)]
    struct Simple {
        value: String,
    }

    #[test]
    fn test_save_nested_dataclass() {
        #[derive(Debug, Clone, PartialEq, Serialize, Deserialize)]
        struct Parent {
            nested: Simple,
        }
        let data = Parent { nested: Simple { value: "B".into() } };
        let json = serde_json::to_string(&data).unwrap();
        let p2: Parent = serde_json::from_str(&json).unwrap();
        assert_eq!(data, p2);
    }

    #[test]
    fn test_nested_list_public() {
        #[derive(Debug, Clone, PartialEq, Serialize, Deserialize)]
        struct Parent {
            nested: Vec<Simple>,
        }
        let data = Parent { nested: vec![Simple { value: "B".into() }, Simple { value: "C".into() }] };
        let json = serde_json::to_string(&data).unwrap();
        let p2: Parent = serde_json::from_str(&json).unwrap();
        assert_eq!(data, p2);
    }

    #[test]
    fn test_nested_nullable_public() {
        #[derive(Debug, Clone, PartialEq, Serialize, Deserialize)]
        struct Parent {
            nested: Option<Simple>
        }
        let data = Parent { nested: None };
        let json = serde_json::to_string(&data).unwrap();
        let p2: Parent = serde_json::from_str(&json).unwrap();
        assert_eq!(data, p2);
    }

    #[test]
    fn test_create_source_public() {
        #[derive(Debug, Clone, PartialEq, Serialize, Deserialize)]
        struct SimpleRenamed {
            renamed_value: String,
        }
        let data = SimpleRenamed { renamed_value: "b".into() };
        let json = serde_json::to_string(&data).unwrap();
        let p2: SimpleRenamed = serde_json::from_str(&json).unwrap();
        assert_eq!(data, p2);
    }

    #[test]
    fn test_many_empty_public() {
        #[derive(Debug, Clone, PartialEq, Serialize, Deserialize)]
        struct HelloWorld {
            value: String,
        }
        let d1 = HelloWorld { value: "changed".to_string() };
        let vec = vec![d1.clone()];
        let json = serde_json::to_string(&vec).unwrap();
        let out: Vec<HelloWorld> = serde_json::from_str(&json).unwrap();
        assert_eq!(out.len(), 1);
        assert_eq!(out[0], d1);
    }

    #[test]
    fn test_empty_sentinel_nesting_public() {
        #[derive(Debug, Clone, PartialEq, Serialize, Deserialize)]
        struct Foo {
            value: Option<String>,
        }
        #[derive(Debug, Clone, PartialEq, Serialize, Deserialize)]
        struct Parent {
            foo: Foo,
        }
        let p = Parent { foo: Foo { value: Some("modified".into()) } };
        let json = serde_json::to_string(&p).unwrap();
        let o: Parent = serde_json::from_str(&json).unwrap();
        assert_eq!(o.foo.value, Some("modified".to_string()));
    }

    #[test]
    fn test_noninit_fields_public() {
        #[derive(Debug, Clone, PartialEq, Serialize, Deserialize)]
        struct A {
            foo: String,
            #[serde(default)]
            bar: String,
        }
        let data = A { foo: "def".to_string(), bar: "xyz".to_string() };
        let json = serde_json::to_string(&data).unwrap();
        let a2: A = serde_json::from_str(&json).unwrap();
        assert_eq!(a2.foo, "def");
        assert_eq!(a2.bar, "xyz");
    }

    #[test]
    fn test_list_save_public() {
        #[derive(Debug, Clone, PartialEq, Serialize, Deserialize)]
        struct Foo {
            name: String,
        }
        let items = vec![
            Foo { name: "alice".to_string() },
            Foo { name: "eve".to_string() }
        ];
        let json = serde_json::to_string(&items).unwrap();
        let v: Vec<Foo> = serde_json::from_str(&json).unwrap();
        assert_eq!(v.len(), 2);
        assert_eq!(v[0], Foo { name: "alice".to_string() });
        assert_eq!(v[1], Foo { name: "eve".to_string() });
    }
}