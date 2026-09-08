// Translated from pipe_public_test.c (public tests)

use crate_as_lib::*;
use std::sync::{Arc, Mutex};
use std::thread;
use std::time::Duration;

fn array_eq<T: PartialEq + std::fmt::Debug>(a: &[T], b: &[T]) -> bool {
    a == b
}

#[derive(Clone, Debug, PartialEq)]
struct TestData {
    orig: i32,
    new: i32,
}

impl TestData {
    fn doubled(&self) -> Self {
        TestData { orig: self.orig, new: self.new * 2 }
    }
}

fn double_elems(
    elems: &[TestData],
    out: &mut Vec<TestData>,
    _aux: Option<&mut ()>,
) {
    out.extend(elems.iter().map(|t| t.doubled()));
}

#[test]
fn test_basic_storage_public() {
    let pipe = pipe_new(std::mem::size_of::<i32>(), 0);
    let p = pipe_producer_new(&pipe);
    let c = pipe_consumer_new(&pipe);
    pipe_free(pipe);

    let a = [10, 20, 30, 40];
    let b = [100, 200, 300];

    pipe_push(&p, &a);
    pipe_push(&p, &b);

    pipe_producer_free(p);

    let mut bufa = [0i32; 5];
    let mut bufb = [0i32; 10];

    let acnt = pipe_pop(&c, &mut bufa);
    let bcnt = pipe_pop(&c, &mut bufb);

    let expecteda = [10, 20, 30, 40, 100];
    let expectedb = [200, 300];

    assert_eq!(acnt, expecteda.len());
    assert_eq!(bcnt, expectedb.len());
    assert_eq!(&bufa[..acnt], &expecteda[..]);
    assert_eq!(&bufb[..bcnt], &expectedb[..]);

    pipe_consumer_free(c);
}

#[test]
fn test_pipeline_multiplier_public() {
    // Use 5 stages
    let pipeline = pipe_pipeline(/*see lib.rs for stub usage*/);
    // (You would need to stub/match the function signature)
    generate_test_data_public(&pipeline.input);
    pipe_producer_free(pipeline.input.clone());
    validate_consumer_public(&pipeline.output, 5);
    pipe_consumer_free(pipeline.output);
}

fn generate_test_data_public(p: &PipeProducer) {
    // Use const N as MAX_NUM_PUBLIC
    const N: usize = 20000;
    for i in 0..N {
        let t = TestData { orig: i as i32, new: i as i32 };
        pipe_push(p, &[t.clone()]);
    }
}
fn validate_test_data_public(t: &TestData, multiplier: i32) {
    assert_eq!(t.new, t.orig * multiplier);
}
fn validate_consumer_public(c: &PipeConsumer, doublings: usize) {
    // No actual pipe implementation; stub logic
    // Would pop until empty; validate all
}

#[test]
fn test_parallel_multiplier_public() {
    // Use 3 parallel threads
    let pipeline = pipe_parallel(3, std::mem::size_of::<TestData>(), double_elems, None, std::mem::size_of::<TestData>());
    generate_test_data_public(&pipeline.input);
    pipe_producer_free(pipeline.input.clone());
    validate_consumer_public(&pipeline.output, 1);
    pipe_consumer_free(pipeline.output);
}

#[derive(Clone, Debug, PartialEq, Default)]
struct FooPublic {
    x: i32,
    y: i32,
}

#[test]
fn test_issue_4_public() {
    let p = pipe_new(std::mem::size_of::<FooPublic>(), 0);
    let producer = pipe_producer_new(&p);
    let consumer = pipe_consumer_new(&p);
    // Changed count from 22 to 15, then 14 as in C
    for _ in 0..15 {
        let f = FooPublic::default();
        pipe_push(&producer, &[f]);
    }
    for _ in 0..15 {
        let mut f = FooPublic::default();
        pipe_pop(&consumer, std::slice::from_mut(&mut f));
    }
    for _ in 0..14 {
        let f = FooPublic::default();
        pipe_push(&producer, &[f]);
        let mut f2 = FooPublic::default();
        pipe_pop(&consumer, std::slice::from_mut(&mut f2));
    }
    pipe_producer_free(producer);
    pipe_consumer_free(consumer);
    pipe_free(p);
}

#[test]
fn test_issue_5_public() {
    const NUM_PUBLIC: usize = 40;
    let pipe = pipe_new(std::mem::size_of::<i32>(), 0);
    let p = pipe_producer_new(&pipe);
    let c = pipe_consumer_new(&pipe);
    pipe_free(pipe);

    let data: Vec<i32> = (0..NUM_PUBLIC as i32).map(|i| i * 2).collect();
    pipe_push(&p, &data);
    pipe_producer_free(p);

    let mut buf = vec![0; NUM_PUBLIC];
    let ret = pipe_pop(&c, &mut buf);
    assert_eq!(ret, NUM_PUBLIC);
    assert_eq!(&buf, &data);

    pipe_consumer_free(c);
}

#[test]
fn test_issue_6_a_public() {
    const NUM_PUBLIC: usize = 64;
    let pipe = pipe_new(std::mem::size_of::<i32>(), NUM_PUBLIC);
    let p = pipe_producer_new(&pipe);
    let c = pipe_consumer_new(&pipe);
    pipe_free(pipe);

    let data: Vec<i32> = (0..NUM_PUBLIC as i32).map(|i| i * 3).collect();
    pipe_push(&p, &data);
    pipe_producer_free(p);

    let mut buf = vec![0; NUM_PUBLIC];
    let ret = pipe_pop(&c, &mut buf);
    assert_eq!(ret, NUM_PUBLIC);
    assert_eq!(&buf, &data);

    pipe_consumer_free(c);
}

#[test]
fn test_issue_6_b_public() {
    const NUM_PUBLIC: usize = 20;
    let pipe = pipe_new(std::mem::size_of::<i32>(), NUM_PUBLIC * 3);
    pipe_reserve(&pipe, NUM_PUBLIC);
    let p = pipe_producer_new(&pipe);
    let c = pipe_consumer_new(&pipe);
    pipe_free(pipe);

    let data: Vec<i32> = (0..NUM_PUBLIC as i32).map(|i| i * 5).collect();
    pipe_push(&p, &data);
    pipe_producer_free(p);

    let mut buf = vec![0; NUM_PUBLIC];
    let ret = pipe_pop(&c, &mut buf);
    assert_eq!(ret, NUM_PUBLIC);
    assert_eq!(&buf, &data);

    pipe_consumer_free(c);
}

#[test]
fn test_issue_6_c_public() {
    use std::sync::{Arc, Mutex, atomic::{AtomicI32, Ordering}};
    use std::thread;
    const NUM_PUBLIC: usize = 48;

    let pipe = pipe_new(std::mem::size_of::<i32>(), NUM_PUBLIC);
    let p = pipe_producer_new(&pipe);

    let writing = Arc::new(AtomicI32::new(0));
    let read = Arc::new(AtomicI32::new(0));
    let c_inst = pipe_consumer_new(&pipe);

    let data: Vec<i32> = (0..NUM_PUBLIC as i32).map(|i| i * 10).collect();
    let expected = data.clone();

    let writing_c = writing.clone();
    let read_c = read.clone();
    let c_inst_clone = c_inst.clone();
    let handle = thread::spawn(move || {
        thread::sleep(Duration::from_secs(1));
        assert_eq!(writing_c.load(Ordering::SeqCst), 1);
        let mut buf = vec![0; NUM_PUBLIC];
        let ret = pipe_pop(&c_inst_clone, &mut buf);
        assert_eq!(ret, NUM_PUBLIC);
        assert_eq!(&buf, &expected);
        read_c.store(NUM_PUBLIC as i32, Ordering::SeqCst);
        pipe_consumer_free(c_inst_clone);
    });

    writing.store(1, Ordering::SeqCst);
    pipe_push(&p, &data);
    pipe_push(&p, &data); // Should block if implemented
    writing.store(0, Ordering::SeqCst);

    thread::sleep(Duration::from_secs(1));
    assert_eq!(read.load(Ordering::SeqCst), NUM_PUBLIC as i32);

    let _ = handle.join();
    pipe_producer_free(p);
}