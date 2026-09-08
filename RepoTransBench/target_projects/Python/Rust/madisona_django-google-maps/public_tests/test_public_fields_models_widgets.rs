#[cfg(test)]
mod public_fields_models_widgets {
    // 1. FakeGeoPtField structure
    struct FakeGeoPtField;

    impl FakeGeoPtField {
        fn to_python(&self, value: &str) -> Option<(f64, f64)> {
            if value.is_empty() {
                return None;
            }
            let pieces: Vec<&str> = value.split(',').collect();
            if pieces.len() != 2 {
                return None;
            }
            Some((
                pieces[0].trim().parse::<f64>().unwrap(),
                pieces[1].trim().parse::<f64>().unwrap()
            ))
        }

        fn get_prep_value(&self, value: (f64, f64)) -> String {
            format!("{:.8},{:.8}", value.0, value.1)
        }

        fn get_prep_value_str(&self, value: &str) -> String {
            value.to_string()
        }
    }

    #[test]
    fn test_geoptfield_to_python_and_get_prep_value_public() {
        let f = FakeGeoPtField;
        let raw_val = "1.111,-2.222";
        let py_val = f.to_python(raw_val).unwrap();
        assert_eq!(py_val, (1.111, -2.222));
        assert_eq!(f.get_prep_value((3.333, -4.444)), "3.33300000,-4.44400000");
    }

    #[test]
    fn test_models_address_and_location_field_repr_and_str_public() {
        struct DummyAddressField { max_length: u32 }
        impl std::fmt::Display for DummyAddressField {
            fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
                write!(f, "DummyAddressField")
            }
        }
        impl std::fmt::Debug for DummyAddressField {
            fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
                write!(f, "DummyAddressField(max_length={})", self.max_length)
            }
        }
        struct DummyLocationField { max_length: u32 }
        impl std::fmt::Display for DummyLocationField {
            fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
                write!(f, "DummyLocationField")
            }
        }
        impl std::fmt::Debug for DummyLocationField {
            fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
                write!(f, "DummyLocationField(max_length={})", self.max_length)
            }
        }
        let fields_and_vals: Vec<(Box<dyn std::fmt::Display>, &str)> = vec![
            (Box::new(DummyAddressField{max_length: 150}), "456 road ave"),
            (Box::new(DummyLocationField{max_length: 150}), "85.63,-172.54"),
        ];
        for (field, _val) in fields_and_vals {
            assert!(format!("{}", field).is_ascii());
            assert!(format!("{:?}", field).is_ascii());
        }
    }

    #[test]
    fn test_widgets_render_attrs_instantiation_public() {
        struct DummyMapWidget { attrs: Option<std::collections::HashMap<String, String>> }
        impl DummyMapWidget {
            fn render(&self, name: &str, value: &str, attrs: Option<&std::collections::HashMap<String, String>>) -> String {
                let mut attrs_str = String::new();
                if let Some(attrs) = attrs {
                    attrs_str.push_str(&format!("{:?}", attrs));
                }
                format!("<input type=\"text\" name=\"{}\" value=\"{}\" {}>", name, value, attrs_str)
            }
        }
        let mut initial_attrs = std::collections::HashMap::new();
        initial_attrs.insert("placeholder".to_owned(), "Enter city".to_owned());
        let map_widget = DummyMapWidget { attrs: Some(initial_attrs.clone()) };
        let mut attrs = std::collections::HashMap::new();
        attrs.insert("id".to_owned(), "map-field".to_owned());
        let html = map_widget.render("sample_location", "21.44,13.33", Some(&attrs));
        assert!(html.contains("sample_location"));
        assert!(html.contains("21.44,13.33"));
        assert!(html.contains("id"));
        assert!(!html.contains("placeholder"));
    }

    #[test]
    fn test_custom_clean_validation_public() {
        struct DummyGeoPtField;
        impl DummyGeoPtField {
            fn clean(&self, value: &str) -> Result<(f64, f64), &'static str> {
                let pieces: Vec<&str> = value.split(',').collect();
                if pieces.len() != 2 {
                    return Err("invalid");
                }
                Ok((
                    pieces[0].parse::<f64>().map_err(|_|"invalid")?,
                    pieces[1].parse::<f64>().map_err(|_|"invalid")?
                ))
            }
            fn clean_tuple(&self, value: (f64, f64)) -> Result<(f64, f64), &'static str> {
                Ok(value)
            }
        }
        let field = DummyGeoPtField;
        assert_eq!(field.clean_tuple((12.34, -56.78)).unwrap(), (12.34, -56.78));
        assert_eq!(field.clean("0.987,-0.654").unwrap(), (0.987, -0.654));
        assert!(field.clean("notacoord").is_err());
        // now test error for a tuple with 1 element (simulate as error)
        // in Rust, can't really call with tuple of 1 element, so test another error:
        assert!(DummyGeoPtField.clean(&field, "1.2").is_err());
    }
}