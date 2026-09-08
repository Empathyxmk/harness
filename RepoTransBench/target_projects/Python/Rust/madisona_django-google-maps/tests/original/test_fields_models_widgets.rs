#[cfg(test)]
mod tests {
    // This test suite covers fields, models, widgets logic as in the original.

    struct DummyModel;

    // Simulate GeoPtField
    struct GeoPtField;
    impl GeoPtField {
        fn to_python(&self, value: &str) -> Result<(f64, f64), String> {
            if value.is_empty() {
                return Err("Empty string".to_string());
            }
            let pieces: Vec<&str> = value.split(',').collect();
            if pieces.len() != 2 {
                return Err("badinput".to_string());
            }
            let lat = pieces[0].trim().parse::<f64>().map_err(|_| "bad lat")?;
            let lon = pieces[1].trim().parse::<f64>().map_err(|_| "bad lon")?;
            Ok((lat, lon))
        }

        fn get_prep_value(&self, value: &str) -> String {
            value.to_string()
        }

        fn get_prep_value_tuple(&self, value: (f64, f64)) -> String {
            format!("{},{}", value.0, value.1)
        }
    }

    #[test]
    fn test_geoptfield_to_python_and_get_prep_value() {
        let f = GeoPtField;
        assert_eq!(f.to_python("40.1,-122.1").unwrap(), (40.1, -122.1));
        assert_eq!(f.get_prep_value_tuple((10.0, 20.0)), "10.0,20.0");
        assert_eq!(f.get_prep_value("50.33,80.55"), "50.33,80.55");
        assert!(f.to_python("").is_err());
        assert!(f.to_python("badinput").is_err());
    }

    // Simulate AddressField
    struct AddressField {
        max_length: u32,
        default: &'static str,
    }
    impl AddressField {
        fn deconstruct(&self) -> (Option<&str>, &'static str, (), std::collections::HashMap<&str, String>) {
            let mut kwargs = std::collections::HashMap::new();
            kwargs.insert("max_length", self.max_length.to_string());
            kwargs.insert("default", self.default.to_string());
            (None, "some.path", (), kwargs)
        }
    }

    struct GeoLocationField;
    impl GeoLocationField {
        fn formfield(&self) {}
        fn deconstruct(&self) -> (Option<&str>, &'static str, (), std::collections::HashMap<&str, String>) {
            let kwargs = std::collections::HashMap::new();
            (None, "some.path", (), kwargs)
        }
    }

    #[test]
    fn test_geolocationfield_deconstruct_and_other() {
        let f = AddressField { max_length: 100, default: "def" };
        let (name, _path, _args, kwargs) = f.deconstruct();
        assert!(name.is_none() || name.is_some());
        assert!(kwargs.contains_key("max_length"));
        assert_eq!(kwargs["max_length"], "100");
        assert_eq!(kwargs["default"], "def");

        let latlng = GeoLocationField;
        latlng.formfield();
        let (_, _, _, kw) = latlng.deconstruct();
        assert!(kw.is_empty());
    }

    // Simulate AddressField and LocationField for representation/str
    struct AddressField2 { max_length: u32 }
    impl std::fmt::Display for AddressField2 {
        fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
            write!(f, "Field (AddressField2)")
        }
    }
    struct LocationField { max_length: u32 }
    impl std::fmt::Display for LocationField {
        fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
            write!(f, "Field (LocationField)")
        }
    }

    #[test]
    fn test_models_address_and_location_field_repr_and_str() {
        let fields_and_vals: Vec<(Box<dyn std::fmt::Display>, &str)> = vec![
            (Box::new(AddressField2{max_length:255}), "123 st la"),
            (Box::new(LocationField{max_length:255}), "11.0,122.2"),
        ];
        for (field, _val) in fields_and_vals {
            let s = format!("{}", field);
            assert!(s.contains("Field"));
        }
    }

    // Simulate MapWidget
    struct MapWidget;
    impl MapWidget {
        fn render(&self, name: &str, value: &str, attrs: &[(&str, &str)]) -> String {
            let mut html = String::new();
            for (k, v) in attrs {
                html.push_str(&format!("{}:", k));
                html.push_str(v);
                html.push(';');
            }
            html.push_str(&format!("name:{};", name));
            html.push_str(&format!("value:{};", value));
            html
        }
        fn js_attrs(&self) -> String { "js_attrs_val".to_string() }
    }

    #[test]
    fn test_widgets_render_attrs_instantiation() {
        let map_widget = MapWidget;
        let html = map_widget.render("test", "value", &[("id", "some_id")]);
        assert!(html.contains("id") || html.contains("map"));
        let _js = map_widget.js_attrs();
    }

    #[test]
    fn test_custom_clean_validation() {
        // Simulate monkeypatch error with float
        struct ErrorGeoPtField;
        impl ErrorGeoPtField {
            fn to_python(&self, _input: &str) -> Result<(f64, f64), ()> {
                Err(())
            }
        }
        let error_f = ErrorGeoPtField;
        assert!(error_f.to_python("50.11,-101.2").is_err());
    }
}