use vijos_jd4::compare::{compare_stream};

fn cmp(a: &[u8], b: &[u8]) -> bool {
    compare_stream(a, b)
}

#[test]
fn test_small() {
    assert!(cmp(b"", b""));
    assert!(cmp(b"a", b"a"));
    assert!(!cmp(b"a", b"b"));
    assert!(cmp(b"bar", b"bar"));
    assert!(!cmp(b"bar", b"baz"));
}

#[test]
fn test_large() {
    assert!(cmp(&vec![b'a'; 1048576], &vec![b'a'; 1048576]));
    let mut a1 = vec![b'a'; 1048576];
    let mut b1 = vec![b'a'; 1048575];
    b1.push(b'b');
    assert!(!cmp(&a1, &b1));
    assert!(cmp(
        &[vec![b'a'; 1048576], vec![b' ', b'b'; 1048576].concat(), b"\r\n".to_vec()].concat(),
        &[vec![b'a'; 1048576], vec![b' '; 1048576], vec![b'b'; 1048576]].concat()
    ));
}