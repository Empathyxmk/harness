#[test]
fn test_fruit_public_fixture() {
    let fruits = ["orange", "grape"];
    for &fruit in &fruits {
        assert!(["orange", "grape"].contains(&fruit));
    }
}