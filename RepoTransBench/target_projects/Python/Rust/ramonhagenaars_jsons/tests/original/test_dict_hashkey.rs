use std::collections::HashMap;

#[derive(Debug, PartialEq, Eq, Hash, Clone)]
struct Foo {
    a: i32,
    b: i32,
    c: i32,
}

#[derive(Debug, PartialEq, Clone)]
struct D {
    a: i32,
    b: i32,
}

fn foo_serializer(obj: &Foo) -> String {
    format!("{},{},{}", obj.a, obj.b, obj.c)
}

fn foo_deserializer(obj: &str) -> Foo {
    let res: Vec<i32> = obj.split(',').map(|s| s.parse::<i32>().unwrap()).collect();
    Foo { a: res[0], b: res[1], c: res[2] }
}

#[test]
fn test_dict_hashkey_with_serializer() {
    // In Rust, simulate registering serializer/deserializer and doing the dump/load
    let bar = HashMap::from([(Foo { a: 1, b: 2, c: 3 }, D { a: 42, b: 39 })]);
    // Serialize keys
    let dumped: HashMap<String, HashMap<&str, i32>> = bar
        .iter()
        .map(|(k, v)| (foo_serializer(k), HashMap::from([("a", v.a), ("b", v.b)])))
        .collect();
    assert_eq!(dumped.get("1,2,3"), Some(&HashMap::from([("a", 42), ("b", 39)])));
    // Deserialize back
    let loaded: HashMap<Foo, D> = dumped
        .iter()
        .map(|(k, v)| (foo_deserializer(k), D { a: *v.get("a").unwrap(), b: *v.get("b").unwrap() }))
        .collect();
    assert_eq!(loaded, bar);
}

#[test]
fn test_dict_hashkey() {
    let bar = HashMap::from([(Foo { a: 1, b: 2, c: 3 }, D { a: 42, b: 39 })]);
    // Serialize keys as string
    let dumped: HashMap<String, HashMap<&str, i32>> = bar.iter()
        .map(|(k, v)| (foo_serializer(k), HashMap::from([("a", v.a), ("b", v.b)])))
        .collect();
    // Deserialize back
    let loaded: HashMap<Foo, D> = dumped
        .iter()
        .map(|(k, v)| (foo_deserializer(k), D { a: *v.get("a").unwrap(), b: *v.get("b").unwrap() }))
        .collect();
    assert_eq!(loaded, bar);
}