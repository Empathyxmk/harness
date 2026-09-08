//! Rust translation of test_map_public.c (public test)

use broadroad_map::map::*;

fn reset_root(root: &mut Root) {
    root.rb_node = None;
}

#[test]
fn test_map_public_basic() {
    let mut mytree = Root { rb_node: None };

    // Empty Tree Lookup (different key)
    let ret = get(&mytree, "hello");
    assert!(ret.is_none(), "get from empty tree should return None");

    // Insertion (new)
    let put_ret = put(&mut mytree, "hello", "world");
    assert_eq!(put_ret, 1, "put (insert)");

    // Lookup existing
    let ret = get(&mytree, "hello");
    assert!(
        ret.is_some() && ret.unwrap().val == "world",
        "get after put"
    );

    // Update existing key
    let put_ret = put(&mut mytree, "hello", "earth");
    assert_eq!(put_ret, 0, "put (update)");

    let ret = get(&mytree, "hello");
    assert!(
        ret.is_some() && ret.unwrap().val == "earth",
        "get after update"
    );

    // Insert more keys (different set)
    put(&mut mytree, "banana", "b1");
    put(&mut mytree, "yak", "y1");
    put(&mut mytree, "blueberry", "bb1");

    // Right branch
    let ret = get(&mytree, "yak");
    assert!(
        ret.is_some() && ret.unwrap().val == "y1",
        "get yak"
    );
    // Left branch
    let ret = get(&mytree, "banana");
    assert!(
        ret.is_some() && ret.unwrap().val == "b1",
        "get banana"
    );
    let ret = get(&mytree, "blueberry");
    assert!(
        ret.is_some() && ret.unwrap().val == "bb1",
        "get blueberry"
    );

    // Lookup non-existent
    let ret = get(&mytree, "not_found");
    assert!(ret.is_none(), "get non-existent");

    // Iteration
    let mut count = 0;
    let mut hello_found = false;
    let mut banana_found = false;
    let mut yak_found = false;
    let mut blueberry_found = false;

    let mut iter = map_first(&mytree);
    while let Some(entry) = iter {
        if entry.key == "hello" { hello_found = true }
        if entry.key == "banana" { banana_found = true }
        if entry.key == "yak" { yak_found = true }
        if entry.key == "blueberry" { blueberry_found = true }
        count += 1;
        iter = map_next(entry);
    }
    assert!(count >= 4 && hello_found && banana_found && yak_found && blueberry_found, "iteration");

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

    println!("All map/basic rbtree PUBLIC tests pass");
}