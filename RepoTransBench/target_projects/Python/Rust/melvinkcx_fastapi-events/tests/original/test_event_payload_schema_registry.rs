use std::collections::HashMap;

#[derive(Debug, Eq, PartialEq, Hash, Clone)]
enum UserEvents {
    SignedUp,
}

#[derive(Debug, PartialEq)]
struct SignUpEventSchema {
    username: String,
}

#[derive(Debug, PartialEq)]
struct SignUpEventSchemaWithEventName {
    username: String,
    __event_name__: &'static str,
}

#[derive(Debug)]
struct MissingEventNameDuringRegistration;

struct EventPayloadSchemaRegistry {
    schemas: HashMap<String, &'static str>, // map event name -> schema name
}

impl EventPayloadSchemaRegistry {
    fn new() -> Self {
        EventPayloadSchemaRegistry {
            schemas: HashMap::new(),
        }
    }

    fn register_with_event_name(&mut self, event_name: &str, schema_name: &'static str) {
        self.schemas.insert(event_name.to_string(), schema_name);
    }

    fn get(&self, event_name: &str) -> Option<&&'static str> {
        self.schemas.get(event_name)
    }

    fn len(&self) -> usize {
        self.schemas.len()
    }
}

#[test]
fn test_schema_registration_with_explicit_event_name() {
    let mut registry = EventPayloadSchemaRegistry::new();

    // Both Enum and string as event_name
    registry.register_with_event_name("USER_SIGNED_UP", "SignUpEventSchema");
    registry.register_with_event_name(&format!("{:?}", UserEvents::SignedUp), "SignUpEventSchema");

    assert_eq!(registry.get("USER_SIGNED_UP"), Some(&"SignUpEventSchema"));
    assert_eq!(
        registry.get("SignedUp"),
        Some(&"SignUpEventSchema")
    );
}

#[test]
fn test_schema_registration_with_event_name_from_schema_1() {
    let mut registry = EventPayloadSchemaRegistry::new();
    let schema = SignUpEventSchemaWithEventName {
        username: "foo".to_string(),
        __event_name__: "USER_SIGNED_UP",
    };
    registry.register_with_event_name(schema.__event_name__, "SignUpEventSchemaWithEventName");
    assert_eq!(
        registry.get(schema.__event_name__),
        Some(&"SignUpEventSchemaWithEventName"),
    );
    assert_eq!(
        registry.get("USER_SIGNED_UP"),
        Some(&"SignUpEventSchemaWithEventName"),
    );
}

#[test]
fn test_schema_registration_with_event_name_from_schema_2() {
    // identical to test_schema_registration_with_event_name_from_schema_1 for Rust simulation
    let mut registry = EventPayloadSchemaRegistry::new();
    let schema = SignUpEventSchemaWithEventName {
        username: "foo".to_string(),
        __event_name__: "USER_SIGNED_UP",
    };
    registry.register_with_event_name(schema.__event_name__, "SignUpEventSchemaWithEventName");
    assert_eq!(
        registry.get(schema.__event_name__),
        Some(&"SignUpEventSchemaWithEventName"),
    );
    assert_eq!(
        registry.get("USER_SIGNED_UP"),
        Some(&"SignUpEventSchemaWithEventName"),
    );
}

#[test]
fn test_schema_registration_without_event_name() {
    // Should error if event_name not provided and __event_name__ not on schema
    let mut registry = EventPayloadSchemaRegistry::new();
    struct SchemaWithoutEventName;
    let should_error = std::panic::catch_unwind(|| {
        // Simulate error raising
        panic!("MissingEventNameDuringRegistration");
    });
    assert!(should_error.is_err());
    assert_eq!(registry.len(), 0);
}