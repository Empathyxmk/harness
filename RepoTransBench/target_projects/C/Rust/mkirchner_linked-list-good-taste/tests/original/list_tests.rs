//! These tests correspond to src/test_list.c from the original C project.

use linked_list_good_taste::{List, ListItem};

#[test]
fn test_insert_and_size() {
    // Setup items
    let mut i1 = ListItem::new(1);
    let mut i2 = ListItem::new(2);
    let mut i3 = ListItem::new(3);
    let mut l = List::new();

    // Insert at head (empty list)
    l.insert_before_c(None, &mut i1);
    let head = l.head.as_ref().unwrap();
    assert_eq!(head.value, 1, "First insert failed");
    assert_eq!(l.size(), 1, "Size should be 1");

    // Insert before head (should become new head)
    // Find pointer to current head for insert_before
    let ptr_head = l.head.as_ref().map(|n| &**n);
    l.insert_before_c(ptr_head, &mut i2);
    let head = l.head.as_ref().unwrap();
    assert_eq!(head.value, 2, "Head should now be i2");
    assert_eq!(head.next.as_ref().unwrap().value, 1, "i2->next should be i1");
    assert_eq!(l.size(), 2, "Size should be 2");

    // Insert at end (before None, append as tail)
    l.insert_before_c(None, &mut i3);
    let i1_ref = l.find_ref(1).unwrap();
    let i1_next_val = i1_ref.next.as_ref().unwrap().value;
    assert_eq!(i1_next_val, 3, "i1->next should be i3");
    let i3_ref = l.find_ref(3).unwrap();
    assert_eq!(i3_ref.next, None, "i3 should be last");
    assert_eq!(l.size(), 3, "Size should be 3 after insert at end");
}

#[test]
fn test_remove_cs101() {
    let mut i1 = ListItem::new(4);
    let mut i2 = ListItem::new(5);
    let mut i3 = ListItem::new(6);

    let mut l = List::new();
    // Form list: i1 -> i2 -> i3
    l.insert_before_c(None, &mut i1);
    l.insert_before_c(None, &mut i2);
    l.insert_before_c(None, &mut i3);

    // Now i3 is head, list: 6 -> 5 -> 4, so let's reconstruct as per C order (i1 as head)
    // We want i1 -> i2 -> i3, so clear and manually link for exact match
    l = List::new();
    l.head = Some(Box::new(ListItem {
        value: 4,
        next: Some(Box::new(ListItem {
            value: 5,
            next: Some(Box::new(ListItem::new(6))),
        })),
    }));

    // Remove middle node i2 (value 5)
    let i2_ptr = l.find_ref(5).unwrap();
    l.remove_cs101(i2_ptr);
    let head = l.head.as_ref().unwrap();
    assert_eq!(head.next.as_ref().unwrap().value, 6, "i2 should be removed");
    assert_eq!(head.value, 4, "head should remain i1");
    assert_eq!(l.size(), 2, "Size should be 2 after remove");

    // Remove head i1 (value 4)
    let i1_ptr = l.find_ref(4).unwrap();
    l.remove_cs101(i1_ptr);
    let head = l.head.as_ref().unwrap();
    assert_eq!(head.value, 6, "head should now be i3");
    assert_eq!(l.size(), 1, "Size should be 1 after head remove");
}

#[test]
fn test_remove_elegant() {
    let mut i1 = ListItem::new(7);
    let mut i2 = ListItem::new(8);
    let mut i3 = ListItem::new(9);

    let mut l = List::new();
    // Build: i1 -> i2 -> i3
    l.head = Some(Box::new(ListItem {
        value: 7,
        next: Some(Box::new(ListItem {
            value: 8,
            next: Some(Box::new(ListItem::new(9))),
        })),
    }));

    // Remove i2 (middle, value 8)
    let i2_ptr = l.find_ref(8).unwrap();
    l.remove_elegant(i2_ptr);
    let i1_ref = l.find_ref(7).unwrap();
    assert_eq!(i1_ref.next.as_ref().unwrap().value, 9, "i2 should be removed (elegant)");

    // Remove i1 (head, value 7)
    let i1_ptr = l.find_ref(7).unwrap();
    l.remove_elegant(i1_ptr);
    let head = l.head.as_ref().unwrap();
    assert_eq!(head.value, 9, "head should be i3 (elegant)");
}

#[test]
fn test_remove_last_and_empty() {
    let mut i1 = ListItem::new(33);
    let mut l = List::new();
    l.head = Some(Box::new(ListItem::new(33)));

    // Remove only node
    let only_ptr = l.find_ref(33).unwrap();
    l.remove_cs101(only_ptr);
    assert!(l.head.is_none(), "After removing only node, list should be empty");
    assert_eq!(l.size(), 0, "Size should be 0");

    // Remove_elegant on single element list
    l.head = Some(Box::new(ListItem::new(33)));
    let only_ptr2 = l.find_ref(33).unwrap();
    l.remove_elegant(only_ptr2);
    assert!(l.head.is_none(), "After elegant removing only node, should be empty");
}

#[test]
fn test_insert_empty_append() {
    let mut i1 = ListItem::new(21);
    let mut l = List::new();
    l.insert_before_c(None, &mut i1);
    let head = l.head.as_ref().unwrap();
    assert_eq!(head.value, 21, "insert_before with NULL in empty list should add at head");
    assert!(head.next.is_none(), "Single element list: next should be NULL");
}