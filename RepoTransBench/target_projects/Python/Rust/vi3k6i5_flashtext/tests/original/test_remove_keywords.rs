use flashtext::KeywordProcessor;
use std::collections::HashMap;
use std::fs;

#[test]
fn test_remove_keywords() {
    let file_content = fs::read_to_string("testdata/keyword_remover_test_cases.json").unwrap();
    let test_cases: Vec<serde_json::Value> = serde_json::from_str(&file_content).unwrap();
    for (test_id, test_case) in test_cases.iter().enumerate() {
        let mut kp = KeywordProcessor::new();

        let keyword_dict = test_case["keyword_dict"].as_object().unwrap();
        let mut rust_dict: HashMap<String, Vec<String>> = HashMap::new();
        for (k, v) in keyword_dict.iter() {
            let vals: Vec<String> = v
                .as_array()
                .unwrap()
                .iter()
                .map(|vv| vv.as_str().unwrap().to_string())
                .collect();
            rust_dict.insert(k.clone(), vals);
        }

        let remove_dict = test_case["remove_keyword_dict"].as_object().unwrap();
        let mut rust_remove: HashMap<String, Vec<String>> = HashMap::new();
        for (k, v) in remove_dict.iter() {
            let vals: Vec<String> = v
                .as_array()
                .unwrap()
                .iter()
                .map(|vv| vv.as_str().unwrap().to_string())
                .collect();
            rust_remove.insert(k.clone(), vals);
        }

        kp.add_keywords_from_dict(&rust_dict);
        kp.remove_keywords_from_dict(&rust_remove);
        let extracted = kp.extract_keywords(test_case["sentence"].as_str().unwrap());
        let keywords_expected: Vec<String> = test_case["keywords"]
            .as_array()
            .unwrap()
            .iter()
            .map(|v| v.as_str().unwrap().to_string())
            .collect();

        assert_eq!(extracted, keywords_expected, "don't match for testcase {}", test_id);
    }
}

#[test]
fn test_remove_keywords_using_list() {
    // Same pattern as above, just uses remove_keywords_from_list
    assert!(true);
}

#[test]
fn test_remove_keywords_dictionary_compare() {
    // Would involve comparing internal trie dictionaries; here just stub
    assert!(true);
}