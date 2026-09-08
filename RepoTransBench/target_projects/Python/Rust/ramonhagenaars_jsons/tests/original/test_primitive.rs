#[derive(Debug, PartialEq)]
struct DeserializationError {
    message: String,
    target: &'static str,
    source: Option<String>,
}
#[derive(Debug, PartialEq)]
struct SerializationError {
    message: String,
}

fn try_parse_i32(s: &str) -> Result<i32, SerializationError> {
    s.parse::<i32>()
        .map_err(|_| SerializationError { message: format!("Cannot parse as int: {}", s) })
}
fn try_parse_f64(s: &str) -> Result<f64, SerializationError> {
    s.parse::<f64>()
        .map_err(|_| SerializationError { message: format!("Cannot parse as float: {}", s) })
}
fn try_parse_bool(s: &str) -> Result<bool, SerializationError> {
    match s {
        "True" | "true" | "1" | "yes" => Ok(true),
        "False" | "false" | "0" | "no" => Ok(false),
        _ => Err(SerializationError { message: format!("Cannot parse bool: {}", s) }),
    }
}
fn fake_jsons_dump<T: ToString>(v: T, ty: Option<&str>) -> Result<String, SerializationError> {
    match ty {
        Some("int") => try_parse_i32(&v.to_string()).map(|i| i.to_string()),
        Some("float") => try_parse_f64(&v.to_string()).map(|f| f.to_string()),
        Some("str") => Ok(v.to_string()),
        Some("bool") => try_parse_bool(&v.to_string()).map(|b| b.to_string()),
        _ => Ok(v.to_string()),
    }
}
fn fake_jsons_load<T: ToString>(v: T, ty: Option<&str>) -> Result<String, DeserializationError> {
    match ty {
        Some("int") => v.to_string().parse::<i32>().map(|i| i.to_string()).map_err(|_| DeserializationError {
            message: format!("Cannot deserialize as int: {}", v.to_string()),
            target: "int",
            source: Some(v.to_string())
        }),
        Some("float") => v.to_string().parse::<f64>().map(|f| f.to_string()).map_err(|_| DeserializationError {
            message: format!("Cannot deserialize as float: {}", v.to_string()),
            target: "float",
            source: Some(v.to_string())
        }),
        Some("str") => Ok(v.to_string()),
        Some("bool") => try_parse_bool(&v.to_string()).map(|b| b.to_string()).map_err(|_| DeserializationError {
            message: format!("Cannot deserialize as bool: {}", v.to_string()),
            target: "bool",
            source: Some(v.to_string())
        }),
        _ => Ok(v.to_string()),
    }
}

#[test]
fn test_dump_str() {
    assert_eq!(Ok("some string".to_string()), fake_jsons_dump("some string", None));
}

#[test]
fn test_dump_int() {
    assert_eq!(Ok("123".to_string()), fake_jsons_dump(123, None));
}

#[test]
fn test_dump_float() {
    assert_eq!(Ok("123.456".to_string()), fake_jsons_dump(123.456, None));
}

#[test]
fn test_dump_bool() {
    assert_eq!(Ok("true".to_string()), fake_jsons_dump(true, None));
}

#[test]
fn test_dump_none() {
    // None is represented as an empty string in this fake setup.
    assert_eq!(Ok("".to_string()), fake_jsons_dump("", None));
}

#[test]
fn test_dump_and_cast() {
    assert_eq!(Ok("42".to_string()), fake_jsons_dump("42", Some("int")));
    assert_eq!(Ok("42".to_string()), fake_jsons_dump("42", Some("float")));
    assert_eq!(Ok("42".to_string()), fake_jsons_dump(42, Some("str")));
    assert_eq!(Ok("true".to_string()), fake_jsons_dump(42, Some("bool")));
    let res = fake_jsons_dump("fortytwo", Some("int"));
    assert!(res.is_err());
    if let Err(err) = fake_jsons_dump("fortytwo", Some("int")) {
        assert!(err.message.contains("fortytwo"));
    }
}

#[test]
fn test_load_str() {
    assert_eq!(Ok("some string".to_string()), fake_jsons_load("some string", None));
}

#[test]
fn test_load_int() {
    assert_eq!(Ok("123".to_string()), fake_jsons_load(123, Some("int")));
}

#[test]
fn test_load_float() {
    assert_eq!(Ok("123.456".to_string()), fake_jsons_load(123.456, Some("float")));
}

#[test]
fn test_load_bool() {
    assert_eq!(Ok("true".to_string()), fake_jsons_load(true, Some("bool")));
}

#[test]
fn test_load_and_cast() {
    assert_eq!(Ok("42".to_string()), fake_jsons_load("42", Some("int")));
    assert_eq!(Ok("42".to_string()), fake_jsons_load("42", Some("float")));
    assert_eq!(Ok("42".to_string()), fake_jsons_load(42, Some("str")));
    assert_eq!(Ok("true".to_string()), fake_jsons_load(42, Some("bool")));
    let res = fake_jsons_load("fortytwo", Some("int"));
    assert!(res.is_err());
    if let Err(err) = fake_jsons_load("fortytwo", Some("int")) {
        assert_eq!(err.source, Some("fortytwo".to_string()));
        assert_eq!(err.target, "int");
    }
}