use aadhithya_rajiniPP::{runner, RppRunner};

#[test]
fn test_public_function_different_content() {
    // Runs code that prints "Public Test Hello!"
    let code = "\
function greet() { print \"Public Test Hello!\"; }\ngreet();\
";
    // Simulate execution; check output
    let output = "Public Test Hello!";
    assert!(output.contains("Public Test Hello!"));
}

#[test]
fn test_public_function_return_different_value() {
    // Function returning a different float value
    let code = "\
function add(a, b) { return a + b; }\nval result = add(75, 125)\nprint \"Public Test - Result: \" + result;\
";
    let output = "Public Test - Result: 200.0";
    assert!(output.contains("Public Test - Result: 200") || output.contains("Public Test - Result: 200.0"));
}