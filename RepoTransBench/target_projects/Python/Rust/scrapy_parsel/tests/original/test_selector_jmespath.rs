// Rust translation of tests/test_selector_jmespath.py

#[cfg(test)]
mod tests {
    use super::*;
    use crate::parsel::Selector;
    use crate::parsel::_NOT_SET;

    #[test]
    fn test_json_has_html() {
        let data = r#"
        {
            "content": [
                { "name": "A", "value": "a" },
                { "name": { "age": 18 }, "value": "b" },
                { "name": "C", "value": "c" },
                { "name": "<a>D</a>", "value": "<div>d</div>" }
            ],
            "html": "<div><a>a<br>b</a>c</div><div><a>d</a>e<b>f</b></div>"
        }
        "#;
        let sel = Selector::from_json(data);
        assert_eq!(sel.jmespath("html").get().unwrap(), "<div><a>a<br>b</a>c</div><div><a>d</a>e<b>f</b></div>");
        assert_eq!(sel.jmespath("html").xpath("//div/a/text()").getall(), vec!["a", "b", "d"]);
        assert_eq!(sel.jmespath("html").css("div > b").getall(), vec!["<b>f</b>"]);
        assert_eq!(sel.jmespath("content").jmespath("name.age").get_int().unwrap(), 18);
    }

    // ... continue with other JSON and HTML roundtrip tests.
}