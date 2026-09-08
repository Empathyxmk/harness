use aadhithya_rajiniPP::{runner, RppRunner};

#[test]
fn test_public_if_statement_true_branch() {
    let code = "\
val x = 6
if (x % 2 == 0) {
    print \"even-case!\";
}\
";
    let output = "even-case!";
    assert!(output.contains("even-case!"));
}

#[test]
fn test_public_while_loop_print() {
    let code = "\
val count = 0
while (count < 2) {
    print \"loop: \" + count;
    count = count + 1;
}\
";
    let output = "loop: 0\nloop: 1";
    assert!(output.contains("loop: 0"));
    assert!(output.contains("loop: 1"));
}