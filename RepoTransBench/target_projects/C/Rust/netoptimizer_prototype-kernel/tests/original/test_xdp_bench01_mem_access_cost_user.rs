const XDP_ABORTED: usize = 0;
const XDP_DROP: usize = 1;
const XDP_PASS: usize = 2;
const XDP_TX: usize = 3;
const XDP_ACTION_MAX: usize = XDP_TX + 1;
const XDP_ACTION_MAX_STRLEN: usize = 11;

static XDP_ACTION_NAMES: [&'static str; XDP_ACTION_MAX] = [
    "XDP_ABORTED",
    "XDP_DROP",
    "XDP_PASS",
    "XDP_TX",
];

fn action2str(action: i32) -> Option<&'static str> {
    if action >= 0 && (action as usize) < XDP_ACTION_MAX {
        Some(XDP_ACTION_NAMES[action as usize])
    } else {
        None
    }
}

/// Returns -1 if not found, otherwise returns the action index.
fn parse_xdp_action(action_str: &str) -> i32 {
    for (i, &name) in XDP_ACTION_NAMES.iter().enumerate() {
        let name_slice = &name[..];
        // Compare up to XDP_ACTION_MAX_STRLEN characters (mimics strncmp)
        if action_str.len() == name_slice.len() && name_slice == action_str {
            return i as i32;
        }
    }
    -1
}

fn cstrcmp(a: &str, b: &str) -> i32 {
    // C-style strcmp
    if a == b { 0 } else { 1 }
}

#[test]
fn test_action2str() {
    assert_eq!(cstrcmp(action2str(XDP_ABORTED as i32).unwrap(), "XDP_ABORTED"), 0);
    assert_eq!(cstrcmp(action2str(XDP_DROP as i32).unwrap(), "XDP_DROP"), 0);
    assert_eq!(cstrcmp(action2str(XDP_PASS as i32).unwrap(), "XDP_PASS"), 0);
    assert_eq!(cstrcmp(action2str(XDP_TX as i32).unwrap(), "XDP_TX"), 0);
    assert!(action2str(-1).is_none());
    assert!(action2str(100).is_none());
}

#[test]
fn test_parse_xdp_action() {
    assert_eq!(parse_xdp_action("XDP_ABORTED"), XDP_ABORTED as i32);
    assert_eq!(parse_xdp_action("XDP_DROP"), XDP_DROP as i32);
    assert_eq!(parse_xdp_action("XDP_PASS"), XDP_PASS as i32);
    assert_eq!(parse_xdp_action("XDP_TX"), XDP_TX as i32);
    assert_eq!(parse_xdp_action("INVALID"), -1);
    // Partial string, should fail
    assert_eq!(parse_xdp_action("XDP"), -1);
}