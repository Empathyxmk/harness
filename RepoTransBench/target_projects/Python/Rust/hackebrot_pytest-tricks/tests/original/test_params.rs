#[test]
fn test_fruit_fixture() {
    let fruits = ["apple", "banana"];
    for &fruit in &fruits {
        assert!(["apple", "banana"].contains(&fruit));
    }
}