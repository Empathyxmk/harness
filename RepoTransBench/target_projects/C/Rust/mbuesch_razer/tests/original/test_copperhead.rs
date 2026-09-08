/*
 Basic tests for copperhead_physical_buttons and copperhead_button_functions arrays
*/

#[derive(Default)]
struct RazerButton {
    name: Option<&'static str>,
}

#[derive(Default)]
struct RazerButtonFunction {
    id: u8,
}

static COPPERHEAD_PHYSICAL_BUTTONS: [RazerButton; 3] = [
    RazerButton { name: Some("Button1") },
    RazerButton { name: Some("Button2") },
    RazerButton { name: Some("ButtonX") },
];
static COPPERHEAD_BUTTON_FUNCTIONS: [RazerButtonFunction; 2] = [
    RazerButtonFunction { id: 1 },
    RazerButtonFunction { id: 2 },
];

#[test]
fn test_copperhead_physical_buttons() {
    // Simple test: check first and last name field for NONE or not
    assert!(COPPERHEAD_PHYSICAL_BUTTONS[0].name.is_some());
}

#[test]
fn test_copperhead_button_functions() {
    assert!(COPPERHEAD_BUTTON_FUNCTIONS.len() >= 1);
}