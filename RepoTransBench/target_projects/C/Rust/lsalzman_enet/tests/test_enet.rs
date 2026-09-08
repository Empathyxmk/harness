use enet::*;

#[test]
fn test_enet_add() {
    assert_eq!(enet_add(1, 2), 3);
    assert_eq!(enet_add(-5, 5), 0);
    assert_eq!(enet_add(2000, 3000), 5000);
}

#[test]
fn test_enet_sub() {
    assert_eq!(enet_sub(10, 3), 7);
    assert_eq!(enet_sub(-2, -2), 0);
    assert_eq!(enet_sub(0, 5), -5);
}

#[test]
fn test_enet_div() {
    assert_eq!(enet_div(10, 2), 5);
    assert_eq!(enet_div(8, 0), 0); // test divide by zero
    assert_eq!(enet_div(-9, 3), -3);
}

#[test]
fn test_enet_max() {
    assert_eq!(enet_max(1, 9), 9);
    assert_eq!(enet_max(-3, -2), -2);
    assert_eq!(enet_max(7, 7), 7);
}