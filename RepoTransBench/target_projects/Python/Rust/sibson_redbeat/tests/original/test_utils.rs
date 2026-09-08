use crate::redbeat::decoder::{from_timestamp, to_timestamp};
use chrono::{Utc};

fn test_roundtrip() {
    let now = Utc::now();
    let roundtripped = from_timestamp(to_timestamp(now), None);
    // compare with second granularity
    assert_eq!(now.timestamp(), roundtripped.timestamp());
}

#[test]
fn test_utils_suite() {
    test_roundtrip();
}