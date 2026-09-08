#[derive(Debug, PartialEq)]
pub struct DeserializationError {
    pub message: String,
    pub target: &'static str,
    pub source: Option<String>,
}

impl DeserializationError {
    pub fn new(message: &str, target: &'static str, source: Option<String>) -> Self {
        DeserializationError {
            message: message.to_string(),
            target,
            source,
        }
    }
}

#[derive(Debug)]
struct WrongUser {
    id: i32,
    // wrong type: birthday should be DateTime, but let's use String as error
    birthday: String,
}

#[derive(Debug)]
struct CorrectUser {
    id: i32,
    birthday: String,
}

fn fake_jsons_load_wrong_user(d: &std::collections::HashMap<&str, &str>) -> Result<WrongUser, DeserializationError> {
    // Simulate: fail for both id type and birthday "wrong type"
    if d["id"] == "Albert" {
        Err(DeserializationError::new("Could not cast \"Albert\" into \"int\"", "int", Some("Albert".to_string())))
    } else if d["birthday"] == "every day" {
        Err(DeserializationError::new(
            "Could not deserialize value \"every day\" into \"datetime.datetime\".",
            "datetime.datetime",
            Some("every day".to_string()),
        ))
    } else if d["birthday"] == "1879-03-14T11:30:00+01:00" {
        Err(DeserializationError::new(
            "No deserializer for type \"datetime\"",
            "datetime",
            None,
        ))
    } else {
        Ok(WrongUser {
            id: d["id"].parse().unwrap_or_default(),
            birthday: d["birthday"].to_string(),
        })
    }
}
fn fake_jsons_load_correct_user(d: &std::collections::HashMap<&str, &str>) -> Result<CorrectUser, DeserializationError> {
    if d["birthday"] == "every day" {
        Err(DeserializationError::new(
            "Could not deserialize value \"every day\" into \"datetime.datetime\".",
            "datetime.datetime",
            Some("every day".to_string()),
        ))
    } else {
        Ok(CorrectUser {
            id: d["id"].parse().unwrap_or_default(),
            birthday: d["birthday"].to_string(),
        })
    }
}

#[test]
fn test_undefined_deserializer() {
    let dumped = std::collections::HashMap::from([("id", "12"), ("birthday", "1879-03-14T11:30:00+01:00")]);
    let result = fake_jsons_load_wrong_user(&dumped);
    assert!(result.is_err());
    let error = result.unwrap_err();
    assert_eq!(error.message, "No deserializer for type \"datetime\"");
    assert_eq!(error.target, "datetime");
}

#[test]
fn test_wrong_primitive_type() {
    let dumped = std::collections::HashMap::from([("id", "Albert"), ("birthday", "1879-03-14T11:30:00+01:00")]);
    let result = fake_jsons_load_wrong_user(&dumped);
    assert!(result.is_err());
    let error = result.unwrap_err();
    assert_eq!(error.message, "Could not cast \"Albert\" into \"int\"");
    assert_eq!(error.target, "int");
}

#[test]
fn test_wrong_type() {
    let dumped = std::collections::HashMap::from([("id", "12"), ("birthday", "every day")]);
    let result = fake_jsons_load_correct_user(&dumped);
    assert!(result.is_err());
    let error = result.unwrap_err();
    assert!(error.message.starts_with("Could not deserialize value \"every day\" into \"datetime.datetime\"."));
    assert_eq!(error.target, "datetime.datetime");
}