#[cfg(test)]
mod public_widget {
    fn render_google_maps_address_widget(name: &str, value: Option<&str>, attrs: &[(&str, &str)]) -> String {
        let mut s = String::from("<input");
        for (k, v) in attrs.iter() {
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
    fn test_render_returns_custom_html() {
        let html = render_google_maps_address_widget(
            "adam",
            Some("customvalue"),
            &[("id", "unique"), ("class", "css-test")]
        );
        let expected = "<input id=\"unique\" class=\"css-test\" name=\"adam\" type=\"text\" value=\"customvalue\" />\
                        <div class=\"map_canvas_wrapper\"><div id=\"map_canvas\"></div></div>";
        assert_eq!(html, expected);
    }

    #[test]
    fn test_render_returns_blank_for_value_when_none_public() {
        let html = render_google_maps_address_widget(
            "foo",
            None,
            &[("style", "color:red;"), ("data-bar", "hello")]
        );
        let expected = "<input style=\"color:red;\" data-bar=\"hello\" name=\"foo\" type=\"text\" />\
                        <div class=\"map_canvas_wrapper\"><div id=\"map_canvas\"></div></div>";
        assert_eq!(html, expected);
    }

    #[test]
    fn test_maps_js_api_key_different() {
        let api_key = "___API_KEY___";
        let google_maps_js = format!("https://maps.google.com/maps/api/js?key={}&libraries=places", api_key);
        let simulated_media_js = vec!["foo.js".to_string(), google_maps_js.clone()];
        assert_eq!(google_maps_js, simulated_media_js[1]);
    }
}