use coroutine::*;
use std::cell::RefCell;
use std::rc::Rc;

#[derive(Debug)]
struct TestArgPub {
    counter: i32,
}

#[test]
fn test_basic_lifecycle_public() {
    let mut s = coroutine_open();
    let arg = Rc::new(RefCell::new(TestArgPub { counter: 5 }));
    
    let arg_clone = arg.clone();
    let co = coroutine_new(&mut s, move |s| {
        arg_clone.borrow_mut().counter += 2;
        coroutine_yield(s);
        arg_clone.borrow_mut().counter += 3;
    });
    
    assert!(co >= 0);
    
    // Ready at start
    assert_eq!(coroutine_status(&s, co), CoroutineStatus::Ready);
    
    // Resume first (add 2, yields)
    coroutine_resume(&mut s, co);
    assert_eq!(arg.borrow().counter, 7);
    assert_eq!(coroutine_status(&s, co), CoroutineStatus::Suspend);
    
    // Resume again (add 3, finish)
    coroutine_resume(&mut s, co);
    assert_eq!(arg.borrow().counter, 10);
    assert_eq!(coroutine_status(&s, co), CoroutineStatus::Dead);
    
    coroutine_close(&mut s);
}

#[test]
fn test_multiple_coroutines_public() {
    let mut s = coroutine_open();
    let a1 = Rc::new(RefCell::new(TestArgPub { counter: 5 }));
    let a2 = Rc::new(RefCell::new(TestArgPub { counter: 20 }));
    
    let a1_clone = a1.clone();
    let co1 = coroutine_new(&mut s, move |s| {
        a1_clone.borrow_mut().counter += 2;
        coroutine_yield(s);
        a1_clone.borrow_mut().counter += 3;
    });
    
    let a2_clone = a2.clone();
    let co2 = coroutine_new(&mut s, move |s| {
        a2_clone.borrow_mut().counter += 2;
        coroutine_yield(s);
        a2_clone.borrow_mut().counter += 3;
    });
    
    coroutine_resume(&mut s, co1); // a1.counter == 7
    coroutine_resume(&mut s, co2); // a2.counter == 22
    coroutine_resume(&mut s, co1); // a1.counter == 10
    coroutine_resume(&mut s, co2); // a2.counter == 25
    
    assert_eq!(a1.borrow().counter, 10);
    assert_eq!(a2.borrow().counter, 25);
    assert_eq!(coroutine_status(&s, co1), CoroutineStatus::Dead);
    assert_eq!(coroutine_status(&s, co2), CoroutineStatus::Dead);
    coroutine_close(&mut s);
}

#[test]
fn test_coroutine_dead_status_public() {
    let mut s = coroutine_open();
    let co = coroutine_new(&mut s, |_| {
        // Do nothing, dies immediately
    });
    
    assert_eq!(coroutine_status(&s, co), CoroutineStatus::Ready);
    coroutine_resume(&mut s, co);
    assert_eq!(coroutine_status(&s, co), CoroutineStatus::Dead);
    
    // double resume, safe
    coroutine_resume(&mut s, co);
    coroutine_close(&mut s);
}

#[test]
fn test_coroutine_running_public() {
    let mut s = coroutine_open();
    let co = coroutine_new(&mut s, |s| {
        let id = coroutine_running(s);
        assert!(id >= 0);
        coroutine_yield(s);
    });
    
    assert_eq!(coroutine_running(&s), -1);
    coroutine_resume(&mut s, co);
    assert_eq!(coroutine_running(&s), -1);
    coroutine_resume(&mut s, co);
    assert_eq!(coroutine_running(&s), -1);
    coroutine_close(&mut s);
}

#[test]
fn test_coroutine_new_capacity_public() {
    let mut s = coroutine_open();
    const SPAWN: usize = 20; // different from 18
    let mut ids = vec![0; SPAWN];
    
    for i in 0..SPAWN {
        ids[i] = coroutine_new(&mut s, |_| {
            // Do nothing, dies immediately
        });
        assert!(ids[i] >= 0);
    }
    
    for i in 0..SPAWN {
        coroutine_resume(&mut s, ids[i]);
    }
    
    coroutine_close(&mut s);
}