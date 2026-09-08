fn fizzbuzz(number: i32) -> String {
    let rules = [
        (3 * 5, "FizzBuzz"),
        (3, "Fizz"),
        (5, "Buzz"),
    ];
    for (div_number, substitution) in rules {
        if number % div_number == 0 {
            return substitution.to_string();
        }
    }
    number.to_string()
}

#[test]
fn test_fizzbuzz_cases() {
    let test_cases = [
        (1, "1"),
        (3, "Fizz"),
        (5, "Buzz"),
        (10, "Buzz"),
        (15, "FizzBuzz"),
        (16, "16")
    ];
    for (number, word) in test_cases {
        assert_eq!(fizzbuzz(number), word);
    }
}