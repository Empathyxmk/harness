use protontricks::util::lower_dict_flat;
use std::collections::HashMap;

#[test]
fn test_public_lower_dict() {
    let mut upper_dict = HashMap::new();
    upper_dict.insert("KEY", 10);
    upper_dict.insert("ALPHA", 20);
    upper_dict.insert("Z", "VALUE");
    upper_dict.insert("MiXeD", "Flag");
    upper_dict.insert("foo", "Bar");
    let lowered = lower_dict_flat(&upper_dict);
    assert_eq!(lowered.get("key"), Some(&10));
    assert_eq!(lowered.get("alpha"), Some(&20));
    assert_eq!(lowered.get("z"), Some(&"VALUE"));
    assert_eq!(lowered.get("mixed"), Some(&"Flag"));
    assert_eq!(lowered.get("foo"), Some(&"Bar"));
}