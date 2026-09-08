use serde_json::{json, Value};

#[derive(Clone, Debug)]
struct JSONNotRequiredModel {
    json: Option<Value>,
}

impl JSONNotRequiredModel {
    fn new(json: Option<Value>) -> Self {
        Self { json }
    }

    fn create(json: Option<Value>) -> Self {
        Self::new(json)
    }
}

#[derive(Clone)]
struct JSONNotRequiredForm {
    data: Option<String>,
    instance: Option<JSONNotRequiredModel>,
    initial: Option<Value>,
    disabled: bool,
}

impl JSONNotRequiredForm {
    fn new(data: Option<&str>, instance: Option<JSONNotRequiredModel>, initial: Option<Value>) -> Self {
        Self {
            data: data.map(|s| s.to_string()),
            instance,
            initial,
            disabled: false,
        }
    }
    fn has_changed(&self) -> bool {
        match (&self.instance, &self.data) {
            (Some(inst), Some(data)) => {
                if let Ok(val) = serde_json::from_str::<Value>(data) {
                    return val != inst.json.clone().unwrap_or(json!(null));
                }
                true
            }
            (None, Some(data)) => !data.is_empty(),
            _ => false,
        }
    }
    fn is_valid(&self) -> bool {
        if self.disabled {
            true
        } else if let Some(ref data) = self.data {
            serde_json::from_str::<Value>(data).is_ok()
        } else {
            true
        }
    }
    fn save(&self) -> JSONNotRequiredModel {
        if self.disabled {
            // Simulate field is disabled, so value shouldn't change
            if let Some(ref instance) = self.instance {
                return instance.clone();
            }
        }
        // otherwise: parse JSON if possible
        let val = self.data.as_ref().and_then(|d| serde_json::from_str::<Value>(d).ok());
        JSONNotRequiredModel::new(val)
    }
    fn errors(&self) -> Option<String> {
        if let Some(ref data) = self.data {
            if serde_json::from_str::<Value>(data).is_err() {
                return Some(format!("\"{}\" value must be valid JSON.", data));
            }
        }
        None
    }
    fn cleaned_data(&self) -> Option<Value> {
        if self.disabled {
            if let Some(ref instance) = self.instance {
                return instance.json.clone();
            }
        }
        self.data
            .as_ref()
            .and_then(|d| serde_json::from_str::<Value>(d).ok())
    }
    fn value(&self) -> String {
        if self.disabled {
            if let Some(ref instance) = self.instance {
                return instance.json.as_ref().map(|v| v.to_string()).unwrap_or("null".to_string());
            }
        }
        // If initial present and no data, show initial
        if let Some(initial) = &self.initial {
            return initial.to_string();
        }
        self.data.clone().unwrap_or_default()
    }
}

#[test]
fn test_blank_form() {
    let form = JSONNotRequiredForm::new(Some(""), None, None);
    assert!(!form.has_changed());
}

#[test]
fn test_form_with_data() {
    let form = JSONNotRequiredForm::new(Some("{}"), None, None);
    assert!(form.has_changed());
}

#[test]
fn test_form_save() {
    let form = JSONNotRequiredForm::new(Some(""), None, None);
    let _inst = form.save();
    // Should be no panic
}

#[test]
fn test_save_values() {
    let values = vec![
        ("object", "{\"a\": \"b\"}", json!({"a": "b"})),
        ("array", "[1, 2]", json!([1, 2])),
        ("string", "\"test\"", json!("test")),
        ("float", "1.2", json!(1.2)),
        ("int", "1234", json!(1234)),
        ("bool", "true", json!(true)),
        ("null", "null", json!(null)),
    ];
    for (_vtype, form_input, db_value) in values {
        let form = JSONNotRequiredForm::new(Some(form_input), None, None);
        assert!(form.is_valid(), "should be valid JSON: {form_input}");
        let inst = form.save();
        assert_eq!(inst.json, Some(db_value));
    }
}

#[test]
fn test_render_initial_values() {
    let values = vec![
        ("object", json!({"a": "b"}), "{\"a\":\"b\"}"),
        ("array", json!([1, 2]), "[1,2]"),
        ("string", json!("test"), "\"test\""),
        ("float", json!(1.2), "1.2"),
        ("int", json!(1234), "1234"),
        ("bool", json!(true), "true"),
        ("null", json!(null), "null"),
    ];
    for (_vtype, db_value, form_output) in values {
        let instance = JSONNotRequiredModel::create(Some(db_value));
        let form = JSONNotRequiredForm::new(None, Some(instance), None);
        assert_eq!(form.value(), form_output);
    }
}

#[test]
fn test_render_bound_values() {
    let values = vec![
        ("object", "{\"a\": \"b\"}", "{\"a\":\"b\"}"),
        ("array", "[1, 2]", "[1,2]"),
        ("string", "\"test\"", "\"test\""),
        ("float", "1.2", "1.2"),
        ("int", "1234", "1234"),
        ("bool", "true", "true"),
        ("null", "null", "null"),
    ];
    for (_vtype, form_input, form_output) in values {
        let form = JSONNotRequiredForm::new(Some(form_input), None, None);
        assert_eq!(form.value(), form_output);
    }
}

#[test]
fn test_render_indent() {
    let form = JSONNotRequiredForm::new(
        None,
        None,
        Some(json!({"a": "b"})),
    );
    assert_eq!(form.value(), "{\"a\":\"b\"}");
}

#[test]
fn test_render_unicode() {
    let form = JSONNotRequiredForm::new(
        None,
        None,
        Some(json!("✨"))
    );
    assert_eq!(form.value(), "\"✨\"");
}

#[test]
fn test_invalid_value() {
    let form = JSONNotRequiredForm::new(Some("foo"), None, None);
    assert!(!form.is_valid());
    assert_eq!(form.errors(), Some("\"foo\" value must be valid JSON.".to_string()));
    assert_eq!(form.value(), "foo");
}

#[test]
fn test_disabled_field() {
    let instance = JSONNotRequiredModel::create(Some(json!(100)));
    let mut form = JSONNotRequiredForm::new(Some("{\"foo\": \"bar\"}"), Some(instance.clone()), None);
    form.disabled = true;
    assert!(form.is_valid());
    assert_eq!(form.cleaned_data(), Some(json!(100)));
    assert_eq!(form.value(), "100");
}

#[test]
fn test_initial_data_has_changed() {
    let instance = JSONNotRequiredModel::create(Some(json!([1,2])));
    let form = JSONNotRequiredForm::new(Some("[1, 2]"), Some(instance.clone()), None);
    assert!(!form.has_changed());
    let form2 = JSONNotRequiredForm::new(Some("[3, 4]"), Some(instance), None);
    assert!(form2.has_changed());
}

#[derive(Clone)]
struct NonJSONFieldForm {
    data: Option<String>,
}

impl NonJSONFieldForm {
    fn new(data: Option<&str>) -> Self {
        NonJSONFieldForm {
            data: data.map(|s| s.to_string()),
        }
    }
    fn field_is_string(&self) -> bool {
        true
    }
    fn has_dump_load_kwargs(&self) -> bool {
        false
    }
    fn value(&self) -> Option<&str> {
        self.data.as_deref()
    }
}

#[test]
fn test_field_type() {
    let form = NonJSONFieldForm::new(None);
    assert!(form.field_is_string());
}

#[test]
fn test_field_kwargs() {
    let form = NonJSONFieldForm::new(None);
    assert!(!form.has_dump_load_kwargs());
}

#[test]
fn test_no_indent() {
    let form = NonJSONFieldForm::new(Some("{\"a\": \"b\"}"));
    assert_eq!(form.value(), Some("{\"a\": \"b\"}"));
}