// Translated from: public_tests/test_public_functions.py

use viralogic_py_enumerable::enumerable::Enumerable;

#[test]
fn test_public_constructor() {
    let vals = vec![4, 5, 6];
    let e = Enumerable::from(vals.clone());
    let items: Vec<_> = e.iter().cloned().collect();
    assert_eq!(items, vals);

    let vals2 = vec![8, 9, 10];
    let e2 = Enumerable::from(vals2.clone());
    let items2: Vec<_> = e2.iter().cloned().collect();
    assert_eq!(items2, vals2);

    let chars: Vec<_> = "abc".chars().collect();
    let e3 = Enumerable::from(chars.clone());
    let items3: Vec<_> = e3.iter().cloned().collect();
    assert_eq!(items3, chars);
}

#[test]
fn test_public_iter() {
    let vals = vec![2, 4, 8];
    let e = Enumerable::from(vals.clone());
    let items: Vec<_> = e.iter().cloned().collect();
    assert_eq!(items, vals);

    let tvals = vec![9, 7, 5];
    let e2 = Enumerable::from(tvals.clone());
    let items2: Vec<_> = e2.iter().cloned().collect();
    assert_eq!(items2, tvals);

    let chars: Vec<_> = "xy".chars().collect();
    let e3 = Enumerable::from(chars.clone());
    let items3: Vec<_> = e3.iter().cloned().collect();
    assert_eq!(items3, chars);
}

#[test]
fn test_public_len() {
    let vals = vec![7, 8, 9];
    let e = Enumerable::from(vals.clone());
    assert_eq!(e.len(), 3);

    let e2 = Enumerable::<i32>::from(vec![]);
    assert_eq!(e2.len(), 0);

    let e3 = Enumerable::from("qw".chars().collect::<Vec<_>>());
    assert_eq!(e3.len(), 2);
}

#[test]
fn test_public_get_item() {
    let vals = vec![11, 22, 33];
    let e = Enumerable::from(vals.clone());
    assert_eq!(e.get(1), Some(22));

    let tvals = vec![99, 88, 77];
    let e2 = Enumerable::from(tvals.clone());
    assert_eq!(e2.get(0), Some(99));

    let chars: Vec<_> = "storm".chars().collect();
    let e3 = Enumerable::from(chars.clone());
    assert_eq!(e3.get(2), Some('o'));
}

#[test]
fn test_public_element_at() {
    let vals = vec![100, 200, 300];
    let e = Enumerable::from(vals.clone());
    assert_eq!(e.get(2), Some(300));

    let chars: Vec<_> = "beep".chars().collect();
    let e2 = Enumerable::from(chars.clone());
    assert_eq!(e2.get(1), Some('e'));
}

#[test]
fn test_public_element_at_error() {
    let vals = vec![1];
    let e = Enumerable::from(vals.clone());
    assert_eq!(e.get(5), None);
}