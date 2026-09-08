use ai_models::main_basic;

#[test]
fn test_main_help() {
    match main_basic::_main(vec!["--help"]) {
        Err(0) => {}, // Simulates SystemExit
        _ => panic!("Did not exit on help"),
    }
}

#[test]
fn test_main_models() {
    match main_basic::_main(vec!["--models"]) {
        Err(0) => {},
        _ => panic!("Did not exit on models"),
    }
}

#[test]
fn test_main_verbose_debug() {
    let out = main_basic::_main(vec!["--verbose"]);
    assert!(out.is_ok());
}