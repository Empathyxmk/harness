//! Translated test for public_test_summary.json metadata

#[cfg(test)]
mod tests {
    #[test]
    fn test_public_test_summary_metadata() {
        let json = r#"
        {
            "project_name": "krakjoe_pcov",
            "language": "C",
            "test_results": {
                "existing_tests_found": false,
                "public_tests_generated": true,
                "existing_tests_passed": true,
                "public_tests_passed": true
            },
            "timestamp": "2025-06-23T20:14:45.731793",
            "original_path": "/workspace/verified_repos_v2/C/krakjoe_pcov",
            "public_test_result_path": "/workspace/public_test_results/C/krakjoe_pcov",
            "original_tests": {
                "test_files": [],
                "test_scripts": [
                    "run_tests.sh"
                ],
                "total_original_test_files": 0,
                "found_existing_tests": false
            },
            "public_tests": {
                "test_files": [
                    "tests_public/001_public.phpt",
                    "tests_public/002_public.phpt",
                    "tests_public/003_public.phpt",
                    "tests_public/004_public.phpt",
                    "tests_public/005_public.phpt",
                    "tests_public/006_public.phpt",
                    "tests_public/007_public.phpt",
                    "tests_public/008_public.phpt",
                    "tests_public/009_public.phpt",
                    "tests_public/010_public.phpt",
                    "tests_public/011_public.phpt",
                    "tests_public/012_public.phpt",
                    "tests_public/013_public.phpt",
                    "tests_public/014_public.phpt",
                    "tests_public/015_public.phpt",
                    "tests_public/016_public.phpt",
                    "run_public_tests.sh",
                    "run_public_tests.sh"
                ],
                "test_scripts": [
                    "run_public_tests.sh",
                    "run_public_tests.sh"
                ],
                "total_public_test_files": 18,
                "generated_public_tests": true
            },
            "created_files": [
                "tests_public/001_public.phpt",
                "tests_public/002_public.phpt",
                "tests_public/003_public.phpt",
                "tests_public/004_public.phpt",
                "tests_public/005_public.phpt",
                "tests_public/006_public.phpt",
                "tests_public/007_public.phpt",
                "tests_public/008_public.phpt",
                "tests_public/009_public.phpt",
                "tests_public/010_public.phpt",
                "tests_public/011_public.phpt",
                "tests_public/012_public.phpt",
                "tests_public/013_public.phpt",
                "tests_public/014_public.phpt",
                "tests_public/015_public.phpt",
                "tests_public/016_public.phpt",
                "run_public_tests.sh",
                "run_public_tests.sh"
            ]
        }
        "#;
        let v: serde_json::Value = serde_json::from_str(json).expect("Valid JSON");
        assert_eq!(v["project_name"], "krakjoe_pcov");
        assert!(v["test_results"]["public_tests_passed"].as_bool().unwrap());
        assert!(v["public_tests"]["test_files"].as_array().unwrap().len() > 10);
    }
}