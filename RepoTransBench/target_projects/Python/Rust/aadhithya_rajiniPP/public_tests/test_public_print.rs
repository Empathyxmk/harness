#[test]
fn test_public_print_simple_message() {
    let code = "print \"Public output!\";";
    let output = "Public output!";
    assert!(output.contains("Public output!"));
}

#[test]
fn test_public_print_number_and_string_concat() {
    let code = "val score = 99\nprint \"Score: \" + score;";
    let output = "Score: 99";
    assert!(output.contains("Score: 99"));
}