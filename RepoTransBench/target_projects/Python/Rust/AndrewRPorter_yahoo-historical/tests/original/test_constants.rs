// Translation of tests/test_constants.py, reconstructed with coverage chunk context.
use yahoo_historical::constants;

#[test]
fn test_constants_import() {
    // In Rust, can always 'import' the module if code compiles
    let _ = constants::API_URL;
    let _ = constants::DATE_INTERVALS;
    let _ = constants::ONE_DAY_INTERVAL;
}

#[test]
fn test_url_dict_or_list() {
    // Check for at least one URL-like attribute present & correct type
    let mut found = false;
    let url_keys = vec!["API_URL", "ONE_DAY_INTERVAL"];
    for key in url_keys {
        found = true;
        match key {
            "API_URL" => {
                let v: &str = constants::API_URL;
                assert!(!v.is_empty());
            }
            "ONE_DAY_INTERVAL" => {
                let v: &str = constants::ONE_DAY_INTERVAL;
                assert_eq!(v, "1d");
            }
            _ => {}
        }
    }
    assert!(found, "No URL-like constants found");
    // Confirm types for all
    assert!(constants::API_URL.is_ascii());
    assert!(constants::ONE_DAY_INTERVAL.is_ascii());
    assert!(constants::DATE_INTERVALS.len() > 0);
}

#[test]
fn test_constant_values() {
    // Check constant types and values
    // (Python checks for .URLS or .ONE_DAY_INTERVAL's type)
    let _ = constants::API_URL;
    let _ = constants::ONE_DAY_INTERVAL;
    assert_eq!(constants::ONE_DAY_INTERVAL, "1d");
    assert!(constants::API_URL.contains("yahoo"));
}

#[test]
fn test_constant_module_str() {
    // in Python: isinstance(str(constants), str) + repr
    // In Rust, test Debug/Display for one constant.
    assert_eq!(format!("{}", constants::ONE_DAY_INTERVAL), "1d");
    assert!(format!("{:?}", constants::DATE_INTERVALS).contains("1d"));
}

#[test]
fn test_all_constant_symbols_accounted() {
    // Defensive: ensure all constants are correct type, similar as possible to Python
    assert!(constants::API_URL.is_ascii());
    assert!(constants::ONE_DAY_INTERVAL.is_ascii());
    for v in constants::DATE_INTERVALS.iter() {
        assert!(v.is_ascii());
    }
}

#[test]
fn test_module_dir_subset() {
    // Rust: by using them above, all are accessed statically - confirms presence via type system
    let _ = constants::API_URL;
    let _ = constants::ONE_DAY_INTERVAL;
}