//! These are public tests corresponding to src/test_list_public.c.
//! They use different values/order but same logical cases.

use linked_list_good_taste::{List, ListItem};

#[test]
fn test_insert_and_size_public() {
    let mut i1 = ListItem::new(10);
    let mut i2 = ListItem::new(20);
    let mut i3 = ListItem::new(30);
    let mut l = List::new();

    // Insert at head (empty)
    l.insert_before_c(None, &mut i1);
    let head = l.head.as_ref().unwrap();
    assert_eq!(head.value, 10, "Public: First insert failed");
    assert_eq!(l.size(), 1, "Public: Size should be 1");

    // Insert before head (should become new head)
    let ptr_head = l.head.as_ref().map(|n| &**n);
    l.insert_before_c(ptr_head, &mut i3); // use i3 as new head for test variety
    let head = l.head.as_ref().unwrap();
    assert_eq!(head.value, 30, "Public: Head should now be i3");
    assert_eq!(head.next.as_ref().unwrap().value, 10, "Public: i3->next should be i1");
    assert_eq!(l.size(), 2, "Public: Size should be 2");

    // Insert at end (append as tail using None)
    l.insert_before_c(None, &mut i2);
    let i1_ref = l.find_ref(10).unwrap();
    let i1_next_val = i1_ref.next.as_ref().unwrap().value;
    assert_eq!(i1_next_val, 20, "Public: i1->next should be i2");
    let i2_ref = l.find_ref(20).unwrap();
    assert!(i2_ref.next.is_none(), "Public: i2 should be last");
    assert_eq!(l.size(), 3, "Public: Size should be 3 after insert at end");
}

#[test]
fn test_remove_cs101_public() {
    let mut i1 = ListItem::new(40);
    let mut i2 = ListItem::new(50);
    let mut i3 = ListItem::new(60);

    let mut l = List::new();
    // Form: i1 -> i2 -> i3
    l.head = Some(Box::new(ListItem {
        value: 40,
        next: Some(Box::new(ListItem {
            value: 50,
            next: Some(Box::new(ListItem::new(60))),
        })),
    }));

    // Remove middle node i2 (value 50)
    let i2_ptr = l.find_ref(50).unwrap();
    l.remove_cs101(i2_ptr);
    let head = l.head.as_ref().unwrap();
    assert_eq!(head.next.as_ref().unwrap().value, 60, "Public: i2 should be removed");
    assert_eq!(head.value, 40, "Public: head should remain i1");
    assert_eq!(l.size(), 2, "Public: Size should be 2 after remove");

    // Remove new head i1 (value 40)
    let i1_ptr = l.find_ref(40).unwrap();
    l.remove_cs101(i1_ptr);
    let head = l.head.as_ref().unwrap();
    assert_eq!(head.value, 60, "Public: head should now be i3");
    assert_eq!(l.size(), 1, "Public: Size should be 1 after head remove");
}

#[test]
fn test_remove_elegant_public() {
    let mut l = List::new();
    // i1=70, i2=80, i3=90
    l.head = Some(Box::new(ListItem {
        value: 70,
        next: Some(Box::new(ListItem {
            value: 80,
            next: Some(Box::new(ListItem::new(90))),
        })),
    }));

    // Remove i2 (middle, value 80)
    let i2_ptr = l.find_ref(80).unwrap();
    l.remove_elegant(i2_ptr);
    let i1_ref = l.find_ref(70).unwrap();
    assert_eq!(i1_ref.next.as_ref().unwrap().value, 90, "Public: i2 should be removed (elegant)");

    // Remove i1 (head, value 70)
    let i1_ptr = l.find_ref(70).unwrap();
    l.remove_elegant(i1_ptr);
    let head = l.head.as_ref().unwrap();
    assert_eq!(head.value, 90, "Public: head should be i3 (elegant)");
}

#[test]
fn test_remove_last_and_empty_public() {
    let mut l = List::new();
    l.head = Some(Box::new(ListItem::new(333)));

    // Remove only node (CS101)
    let only_ptr = l.find_ref(333).unwrap();
    l.remove_cs101(only_ptr);
    assert!(l.head.is_none(), "Public: After removing only node, list should be empty");
    assert_eq!(l.size(), 0, "Public: Size should be 0");

    // Remove_elegant on single element list
    l.head = Some(Box::new(ListItem::new(333)));
    let only_ptr2 = l.find_ref(333).unwrap();
    l.remove_elegant(only_ptr2);
    assert!(l.head.is_none(), "Public: After elegant removing only node, should be empty");
}

#[test]
fn test_insert_empty_append_public() {
    let mut i1 = ListItem::new(121);
    let mut l = List::new();
    l.insert_before_c(None, &mut i1);
    let head = l.head.as_ref().unwrap();
    assert_eq!(head.value, 121, "Public: insert_before with None in empty list should add at head");
    assert!(head.next.is_none(), "Public: Single element list: next should be NULL");
}