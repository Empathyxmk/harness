use flashtext::KeywordProcessor;
use std::collections::HashMap;
use std::fs;

#[test]
fn test_remove_keywords_dictionary_len() {
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
        let kp_len = kp.get_all_keywords().len();

        // Now compute reference dict
        let mut new_dictionary = HashMap::new();
        for (key, values) in &rust_dict {
            let mut keep = Vec::new();
            for value in values {
                if !(rust_remove.contains_key(key) && rust_remove[key].contains(value)) {
                    keep.push(value.clone());
                }
            }
            if !keep.is_empty() {
                new_dictionary.insert(key.clone(), keep);
            }
        }

        let mut kp2 = KeywordProcessor::new();
        kp2.add_keywords_from_dict(&new_dictionary);
        let kp2_len = kp2.get_all_keywords().len();
        assert_eq!(
            kp_len, kp2_len,
            "keyword processor length doesn't match for Text ID {}",
            test_id
        );
    }
}