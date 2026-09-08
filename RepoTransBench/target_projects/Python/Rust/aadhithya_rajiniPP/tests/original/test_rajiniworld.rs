use std::collections::HashMap;
use aadhithya_rajiniPP::__rajiniworld__::{__vars__, __functions__};

#[test]
fn test_vars_and_functions_are_dicts() {
    // Should always be maps (dicts)
    // lazily initialized, so we access as HashMap
    let _: &HashMap<&'static str, f64> = &__vars__;
    let _: &HashMap<&'static str, fn()> = &__functions__;
}