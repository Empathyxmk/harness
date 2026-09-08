use homu_rust::mainmod;

#[test]
fn test_process_input_reverse() {
    let result = mainmod::process_input("alpha");
    assert_eq!(result, "ahpla");
}

#[test]
fn test_process_input_palindrome() {
    let result = mainmod::process_input("noon");
    assert_eq!(result, "noon");
}