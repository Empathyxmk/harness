use aadhithya_rajiniPP::__rajiniworld__::{__vars__, __functions__};
use std::collections::HashMap;

#[test]
fn test_public_vars_and_functions_dict_nonempty() {
    let _: &HashMap<&'static str, f64> = &__vars__;
    let _: &HashMap<&'static str, fn()> = &__functions__;
}