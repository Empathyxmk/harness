// Translated from: public_tests/test_public_py_linq_branch.py

use viralogic_py_enumerable::enumerable::Enumerable;

#[test]
fn test_public_select_many_branch() {
    let source = Enumerable::from(vec![vec![1, 2], vec![3]]);
    let r: Vec<_> = source.select_many(|x| x.iter().map(|y| y * 2).collect::<Vec<_>>()).to_list();
    assert_eq!(r, vec![2, 4, 6]);
}

#[test]
fn test_public_select_branch() {
    let source = Enumerable::from(vec![3, 6, 9]);
    let r: Vec<_> = source.select(|x| x * 4).to_list();
    assert_eq!(r, vec![12, 24, 36]);
}