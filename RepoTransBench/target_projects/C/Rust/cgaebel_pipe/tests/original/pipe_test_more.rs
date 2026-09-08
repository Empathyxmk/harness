// Translated from pipe_test_more.c (original/extra tests)

use crate_as_lib::*;
use std::sync::{Arc, Mutex};
use std::thread;
use std::time::Duration;

// Stubs and helpers as in main original test
fn dummy_processor(input: &[i32], out: &mut Vec<i32>, _aux: Option<&mut ()>) {
    if !input.is_empty() && out != &mut Vec::new() {
        out.extend_from_slice(input);
    }
}

#[test]
fn test_trivial_pipeline() {
    let pipe = pipe_new(std::mem::size_of::<i32>(), 0);
    let pl = pipe_trivial_pipeline(&pipe);
    let value = 42;
    let mut output = 0;
    pipe_push(&pl.input, &[value]);
    let mut buf = [0_i32; 1];
    let res = pipe_pop(&pl.output, &mut buf);
    assert_eq!(res, 1);
    assert_eq!(buf[0], 42);
    pipe_producer_free(pl.input);
    pipe_consumer_free(pl.output);
    pipe_free(pipe);
}

// The rest of the tests mirror those in the C code
#[test]
fn test_pipe_parallel() {
    let pl = pipe_parallel(2, std::mem::size_of::<i32>(), dummy_processor, None, std::mem::size_of::<i32>());
    let v = 17;
    let mut buf = [0_i32; 1];
    pipe_push(&pl.input, &[v]);
    let res = pipe_pop(&pl.output, &mut buf);
    assert_eq!(res, 1);
    assert_eq!(buf[0], 17);
    pipe_producer_free(pl.input);
    pipe_consumer_free(pl.output);
}

#[test]
fn test_pipe_connect() {
    let pipe = pipe_new(std::mem::size_of::<i32>(), 0);
    let in_c = pipe_consumer_new(&pipe);
    let out = pipe_producer_new(&pipe);
    pipe_connect(&in_c, dummy_processor, None, &out);
    pipe_producer_free(out);
    pipe_consumer_free(in_c);
    pipe_free(pipe);
}

// The rest: input checks, pop empty, push and close, free null, etc.

#[test]
fn test_pipe_pop_empty() {
    let pipe = pipe_new(std::mem::size_of::<i32>(), 10);
    let c = pipe_consumer_new(&pipe);
    let mut result = [0_i32; 1];
    let rc = pipe_pop(&c, &mut result);
    assert_eq!(rc, 0);
    pipe_consumer_free(c);
    pipe_free(pipe);
}

#[test]
fn test_pipe_push_and_close() {
    let pipe = pipe_new(std::mem::size_of::<i32>(), 2);
    let producer = pipe_producer_new(&pipe);
    let consumer = pipe_consumer_new(&pipe);
    let data = 100;
    let data2 = 200;
    pipe_push(&producer, &[data]);
    pipe_push(&producer, &[data2]);
    pipe_free(pipe);
    pipe_producer_free(producer);
    pipe_consumer_free(consumer);
}

#[test]
fn test_pipe_free_null() {
    // No-op tests, free null pointers
    pipe_free(Pipe {});
    pipe_producer_free(PipeProducer {});
    pipe_consumer_free(PipeConsumer {});
}

// Extra main-thread_ring routines are omitted as main is not used in Rust test harness.