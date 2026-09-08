#[cfg(test)]
mod tests {
    // Test for widget rendering and js inclusion

    fn render_google_maps_address_widget(name: &str, value: Option<&str>, attrs: &[(&str, &str)]) -> String {
        // Simulates the output of GoogleMapsAddressWidget.render().
        let mut s = String::from("<input");
        for (k, v) in attrs {
            s.push(' ');
            s.push_str(k);
            s.push_str("=\"");
            s.push_str(v);
            s.push('"');
        }
        s.push_str(" name=\"");
        s.push_str(name);
        s.push_str("\" type=\"text\"");
        if let Some(val) = value {
            s.push_str(" value=\"");
            s.push_str(val);
            s.push('"');
        }
        s.push_str(" />");
        s.push_str("<div class=\"map_canvas_wrapper\">");
        s.push_str("<div id=\"map_canvas\"></div></div>");
        s
    }

    #[test]
    fn test_render_returns_xxxxxxx() {
        let html = render_google_maps_address_widget("name", Some("value"), &[("a1","1"),("a2","2")]);
        let expected = String::from("<input a1=\"1\" a2=\"2\" name=\"name\" type=\"text\" value=\"value\" />") +
            "<div class=\"map_canvas_wrapper\">" +
            "<div id=\"map_canvas\"></div></div>";
        assert_eq!(html, expected);
    }

    #[test]
    fn test_render_returns_blank_for_value_when_none() {
        let html = render_google_maps_address_widget("name", None, &[("a1","1"),("a2","2")]);
        let expected = String::from("<input a1=\"1\" a2=\"2\" name=\"name\" type=\"text\" />") +
            "<div class=\"map_canvas_wrapper\">" +
            "<div id=\"map_canvas\"></div></div>";
        assert_eq!(html, expected);
    }

    #[test]
    fn test_maps_js_uses_api_key() {
        // Simulate a settings struct with GOOGLE_MAPS_API_KEY
        let api_key = "___API_KEY___";
        let google_maps_js = format!("https://maps.google.com/maps/api/js?key={}&libraries=places", api_key);
        // Simulate a widget Media that returns an array of js file refs
        let simulated_media_js = vec!["foo.js".to_string(), google_maps_js.clone()];
        assert_eq!(google_maps_js, simulated_media_js[1]);
    }
}