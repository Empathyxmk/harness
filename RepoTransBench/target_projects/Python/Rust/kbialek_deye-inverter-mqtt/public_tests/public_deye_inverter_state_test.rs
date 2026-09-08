// Public: Translated from public_tests/public_deye_inverter_state_test.py

#[derive(Debug, PartialEq)]
enum InvState { Running, Idle }

#[test]
fn test_inverter_state_public() {
    let s = InvState::Running;
    assert_eq!(s, InvState::Running);
}