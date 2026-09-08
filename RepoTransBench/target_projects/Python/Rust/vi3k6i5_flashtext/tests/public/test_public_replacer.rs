use flashtext::KeywordProcessor;
use std::collections::HashMap;
use std::fs;
use regex::Regex;

#[test]
fn test_public_replace_keywords() {
    let file_content = fs::read_to_string("testdata/keyword_extractor_test_cases.json").unwrap();
    let test_cases: Vec<serde_json::Value> = serde_json::from_str(&file_content).unwrap();
    for (test_id, test_case) in test_cases.iter().enumerate() {
        let mut kp = KeywordProcessor::new();
        let keyword_dict = test_case["keyword_dict"].as_object().unwrap();
        let mut keyword_mapping = HashMap::new();
        for (clean_key, values) in keyword_dict {
            for value in values.as_array().unwrap() {
                let value_str = value.as_str().unwrap();
                kp.add_keyword(value_str, &clean_key.replace(" ", "_"));
                keyword_mapping.insert(value_str.to_string(), clean_key.replace(" ", "_"));
            }
        }
        let mut replaced_sentence = test_case["sentence"].as_str().unwrap().to_string();

        let mut mapping: Vec<_> = keyword_mapping.clone().into_iter().collect();
        mapping.sort_by(|a, b| b.0.len().cmp(&a.0.len())); // longer matches first

        for (k, v) in mapping {
            let regex_pat = format!(r"(?i)(?<!\w){}(?!\w)", regex::escape(&k));
            let re = Regex::new(&regex_pat).unwrap();
            replaced_sentence = re.replace_all(&replaced_sentence, v.as_str()).to_string();
        }

        let new_sentence = kp.replace_keywords(test_case["sentence"].as_str().unwrap());
        assert_eq!(
            new_sentence, replaced_sentence,
            "new_sentence don't match the expected results for test case: {}",
            test_id
        );
    }
}