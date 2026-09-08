use enet::*;

#[test]
fn test_enet_add_public() {
    assert_eq!(enet_add(8, 15), 23);
    assert_eq!(enet_add(-10, 11), 1);
    assert_eq!(enet_add(5555, 4445), 10000);
}

#[test]
fn test_enet_sub_public() {
    assert_eq!(enet_sub(20, 5), 15);
    assert_eq!(enet_sub(-7, -14), 7);
    assert_eq!(enet_sub(3, 8), -5);
}

#[test]
fn test_enet_div_public() {
    assert_eq!(enet_div(25, 5), 5);
    assert_eq!(enet_div(0, 5), 0); // division of zero
    assert_eq!(enet_div(7, 2), 3);
}

#[test]
fn test_enet_max_public() {
    assert_eq!(enet_max(123, 77), 123);
    assert_eq!(enet_max(-100, -50), -50);
    assert_eq!(enet_max(42, 42), 42);
}