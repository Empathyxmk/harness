use std::fs;
use serde_json::Value;
use flashtext::KeywordProcessor;

#[test]
fn test_extract_keywords() {
    let file_content = fs::read_to_string("testdata/keyword_extractor_test_cases.json").unwrap();
    let test_cases: Vec<Value> = serde_json::from_str(&file_content).unwrap();
    for (test_id, test_case) in test_cases.iter().enumerate() {
        let mut kp = KeywordProcessor::new();
        if let Some(keyword_dict) = test_case.get("keyword_dict") {
            if let Some(map) = keyword_dict.as_object() {
                for (_key, values) in map {
                    // values is an array of strings
                    if let Some(arr) = values.as_array() {
                        for val in arr {
                            kp.add_keyword(&val.as_str().unwrap(), &val.as_str().unwrap());
                        }
                    }
                }
            }
        }
        let sentence = test_case["sentence"].as_str().unwrap();
        let extracted = kp.extract_keywords(sentence);
        // Without span_info support, we use extracted names for now
        let keywords_expected: Vec<String> = test_case["keywords"]
            .as_array()
            .unwrap()
            .iter()
            .map(|v| v.as_str().unwrap().to_string())
            .collect();
        assert_eq!(
            extracted, keywords_expected,
            "keywords span don't match expected results for test case {}",
            test_id
        );
    }
}

// For case_sensitive logic, can duplicate above with case check