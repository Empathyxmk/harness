use homu_rust::mainmod;

#[test]
fn test_process_input_reverse_existing() {
    let result = mainmod::process_input("test");
    assert_eq!(result, "tset");
}

#[test]
fn test_process_input_palindrome_existing() {
    let result = mainmod::process_input("abba");
    assert_eq!(result, "abba");
}

#[test]
fn test_suppress_pings_in_pr_body() {
    let body = "r? @matklad\n@bors r+\nmail@example.com";
    let expected = "r? `@matklad`\n`@bors` r+\nmail@example.com\n";
    assert_eq!(mainmod::suppress_pings(body), expected);
}

#[test]
fn test_suppress_ignore_block_in_pr_body() {
    let body = format!(
        "Rollup merge\n{}\n[Create a similar rollup](https://fake.xyz/?prs=1,2,3)\n{}",
        mainmod::IGNORE_BLOCK_START,
        mainmod::IGNORE_BLOCK_END
    );
    let expect = "Rollup merge\n";
    assert_eq!(mainmod::suppress_ignore_block(&body), expect.to_string());
}