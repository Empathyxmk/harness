fn foobar(number: i32) -> String {
    let public_rules = [
        (2 * 7, "FooBar"),
        (2, "Foo"),
        (7, "Bar"),
    ];
    for (div_number, substitution) in public_rules {
        if number % div_number == 0 {
            return substitution.to_string();
        }
    }
    number.to_string()
}

#[test]
fn test_foobar_cases() {
    let test_cases = [
        (1, "1"),
        (2, "Foo"),
        (7, "Bar"),
        (14, "FooBar"),
        (8, "Foo"),
        (13, "13"),
    ];
    for (number, word) in test_cases {
        assert_eq!(foobar(number), word);
    }
}