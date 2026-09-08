use std::thread;

#[test]
fn test_thread_arg_and_retval_pub() {
    let ids = [101, 202, 303];
    let mut handles = Vec::new();
    for id in &ids {
        let id = *id;
        handles.push(thread::spawn(move || id));
    }
    for (i, h) in handles.into_iter().enumerate() {
        let val = h.join().unwrap();
        assert_eq!(val, ids[i]);
    }
}

thread_local! {
    static GLOCALVAR_PUB: std::cell::Cell<i32> = std::cell::Cell::new(0);
}

#[test]
fn test_thread_local_storage_pub() {
    GLOCALVAR_PUB.with(|x| x.set(1234));
    let handle = thread::spawn(|| {
        GLOCALVAR_PUB.with(|x| x.set(44));
    });
    handle.join().unwrap();
    GLOCALVAR_PUB.with(|x| assert_eq!(x.get(), 1234));
}