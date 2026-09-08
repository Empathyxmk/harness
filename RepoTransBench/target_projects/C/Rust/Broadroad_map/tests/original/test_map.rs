//! Rust translation of the original C test_map.c.

use broadroad_map::map::*;

fn reset_root(root: &mut Root) {
    root.rb_node = None;
}

#[test]
fn test_map_basic() {
    // Setup
    let mut mytree = Root { rb_node: None };

    // Empty Tree Lookup
    let ret = get(&mytree, "foo");
    assert!(ret.is_none(), "get from empty tree should return None");

    // Insertion (new)
    let put_ret = put(&mut mytree, "foo", "bar");
    assert_eq!(put_ret, 1, "put (insert)");

    // Lookup existing
    let ret = get(&mytree, "foo");
    assert!(
        ret.is_some() && ret.unwrap().val == "bar",
        "get after put"
    );

    // Update existing key
    let put_ret = put(&mut mytree, "foo", "baz");
    assert_eq!(put_ret, 0, "put (update)");

    let ret = get(&mytree, "foo");
    assert!(
        ret.is_some() && ret.unwrap().val == "baz",
        "get after update"
    );

    // Insert more keys (left/right branches)
    put(&mut mytree, "apple", "a1");
    put(&mut mytree, "zebra", "z1");
    put(&mut mytree, "aardvark", "aa1");

    // Right branch
    let ret = get(&mytree, "zebra");
    assert!(
        ret.is_some() && ret.unwrap().val == "z1",
        "get zebra"
    );

    // Left branch
    let ret = get(&mytree, "apple");
    assert!(
        ret.is_some() && ret.unwrap().val == "a1",
        "get apple"
    );
    let ret = get(&mytree, "aardvark");
    assert!(
        ret.is_some() && ret.unwrap().val == "aa1",
        "get aardvark"
    );

    // Lookup non-existent
    let ret = get(&mytree, "nomatch");
    assert!(ret.is_none(), "get non-existent");

    // Iteration
    let mut count = 0;
    let mut foo_found = false;
    let mut apple_found = false;
    let mut zebra_found = false;
    let mut aardvark_found = false;

    let mut iter = map_first(&mytree);
    while let Some(entry) = iter {
        if entry.key == "foo" { foo_found = true }
        if entry.key == "apple" { apple_found = true }
        if entry.key == "zebra" { zebra_found = true }
        if entry.key == "aardvark" { aardvark_found = true }
        count += 1;
        iter = map_next(entry);
    }
    assert!(count >= 4 && foo_found && apple_found && zebra_found && aardvark_found, "iteration");

    // Remove all allocated map_t (test freeing and None protection)
    let mut to_free = vec![];
    let mut iter = map_first(&mytree);
    while let Some(entry) = iter {
        if to_free.len() < 4 { to_free.push(entry.clone()); }
        iter = map_next(entry);
    }
    for entry in &to_free {
        map_free(entry);
    }
    map_free(&MapEntry::new("", ""));

    println!("All map/basic rbtree tests pass");
}