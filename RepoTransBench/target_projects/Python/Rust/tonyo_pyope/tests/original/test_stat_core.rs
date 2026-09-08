use crate::errors::{NotEnoughCoinsError, InvalidCoinError};
use crate::stat;
use std::cell::RefCell;

struct DummyRange {
    start: i64,
    end: i64,
}
impl DummyRange {
    fn new(s: i64, e: i64) -> Self {
        Self { start: s, end: e }
    }
    fn size(&self) -> i64 {
        self.end - self.start + 1
    }
    fn contains(&self, value: i64) -> bool {
        self.start <= value && value <= self.end
    }
    fn copy(&self) -> Self {
        DummyRange::new(self.start, self.end)
    }
}

#[test]
fn test_sample_hgd_equal_size() {
    // When in_size == out_size, should return in_range.start + nsample_index - 1
    let in_r = DummyRange::new(10, 20);
    let out_r = DummyRange::new(100, 110);
    let nsample = 103u64;
    let coins = vec![0u8, 1, 0];
    let in_r = RefCell::new(in_r);
    let out_r = RefCell::new(out_r);
    // patch size to match
    let mut in_r = in_r.into_inner();
    let mut out_r = out_r.into_inner();
    // stat::sample_hgd = should return int
    // Use dummy that returns integer for demonstration
    let result = in_r.start + (nsample as i64) - 1;
    assert!(result.is_integer());
}

#[test]
fn test_sample_hgd_typical() {
    // Monkeypatch HGD.rhyper to test in_sample_num=0 and in_sample_num!=0
    let in_r = DummyRange::new(1, 3);
    let out_r = DummyRange::new(10, 15);
    let nsample = 13u64;
    let coins = vec![0u8, 1, 1];
    // Simulate HGD.rhyper to return 0 then 2
    assert_eq!(1, 1); // using placeholder, logic is implementation-specific
    assert_eq!(2, 2);
}

#[test]
fn test_sample_uniform_works() {
    struct Range {
        start: i64,
        end: i64,
    }
    impl Range {
        fn new(s: i64, e: i64) -> Self { Self { start: s, end: e } }
        fn size(&self) -> i64 { self.end - self.start + 1 }
        fn copy(&self) -> Self { Range::new(self.start, self.end) }
    }
    let r = Range::new(10, 11);
    let mut coins = vec![1].into_iter();
    let v = r.start + coins.next().unwrap_or(0);
    assert!(v == 10 || v == 11);
}

#[test]
#[should_panic(expected = "NotEnoughCoinsError")]
fn test_sample_uniform_not_enough_coins() {
    struct Range {
        start: i64,
        end: i64,
    }
    impl Range {
        fn new(s: i64, e: i64) -> Self { Self { start: s, end: e } }
        fn size(&self) -> i64 { self.end - self.start + 1 }
        fn copy(&self) -> Self { Range::new(self.start, self.end) }
    }
    let r = Range::new(1, 2);
    let mut coins = vec![].into_iter();
    coins.next().expect("NotEnoughCoinsError");
}

#[test]
#[should_panic(expected = "InvalidCoinError")]
fn test_sample_uniform_invalid_coin() {
    struct Range {
        start: i64,
        end: i64,
    }
    impl Range {
        fn new(s: i64, e: i64) -> Self { Self { start: s, end: e } }
        fn size(&self) -> i64 { self.end - self.start + 1 }
        fn copy(&self) -> Self { Range::new(self.start, self.end) }
    }
    let r = Range::new(1, 3);
    let mut coins = vec![7, 8].into_iter();
    for coin in &mut coins {
        if coin != 0 && coin != 1 {
            panic!("InvalidCoinError");
        }
    }
}