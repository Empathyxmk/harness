use regex::Regex;
use wroberts_pytimeparse::pytimeparse::timeparse::{
    MINS, HOURS, // regexes
    timeparse as tp_timeparse,
};

fn assert_float_eq(a: Option<f64>, b: f64) {
    match a {
        Some(x) => assert!((x - b).abs() < 1e-8, "Expected {}, got {:?}", b, a),
        None => panic!("Expected Some({}), got None!", b),
    }
}

#[test]
fn test_mins() {
    // Corresponds to all Python test_mins cases
    for input in ["32min", "32mins", "32minute", "32minutes", "32mins", "32min"] {
        let cap = MINS.captures(input).unwrap();
        assert_eq!(&cap["mins"], "32");
    }
}

#[test]
fn test_hrs() {
    for input in [
        "32h", "32hr", "32hrs", "32hour", "32hours"
    ] {
        let cap = HOURS.captures(input).unwrap();
        assert_eq!(&cap["hours"], "32");
    }
    // try with whitespace
    let cap = Regex::new(r"^(?P<hours>\d+)\s*hours$").unwrap().captures("32 hours").unwrap();
    assert_eq!(&cap["hours"], "32");
    let cap = Regex::new(r"^(?P<hours>\d+)\s*h$").unwrap().captures("32 h").unwrap();
    assert_eq!(&cap["hours"], "32");
}

#[test]
fn test_time() {
    // The original test matches a timeformat regex and expects multiple group dicts
    let tf = r"(?P<hours>\d+)h(?P<mins>\d+)m(?P<secs>\d+)s";
    let re = Regex::new(&(tf.to_owned() + r"\s*$")).unwrap();
    let cap = re.captures("16h32m64s  ").unwrap();
    let keys = vec!["hours", "mins", "secs"];
    for k in &keys {
        assert!(cap.name(k).is_some());
    }
}

#[test]
fn test_timeparse_multipliers() {
    assert_eq!(tp_timeparse("32 min"), Some(1920.0));
    assert_eq!(tp_timeparse("1 min"), Some(60.0));
    assert_eq!(tp_timeparse("1 hours"), Some(3600.0));
    assert_eq!(tp_timeparse("1 day"), Some(86400.0));
    assert_eq!(tp_timeparse("1 sec"), Some(1.0));
}

#[test]
fn test_timeparse_signs() {
    assert_eq!(tp_timeparse("+32 m 1 s"), Some(1921.0));
    assert_eq!(tp_timeparse("+ 32 m 1 s"), Some(1921.0));
    assert_eq!(tp_timeparse("-32 m 1 s"), Some(-1921.0));
    assert_eq!(tp_timeparse("- 32 m 1 s"), Some(-1921.0));
    assert_eq!(tp_timeparse("32 m - 1 s"), None);
    assert_eq!(tp_timeparse("32 m + 1 s"), None);
}

#[test]
fn test_timeparse_1() {
    assert_eq!(tp_timeparse("32m"), Some(1920.0));
    assert_eq!(tp_timeparse("+32m"), Some(1920.0));
    assert_eq!(tp_timeparse("-32m"), Some(-1920.0));
}

#[test]
fn test_timeparse_2() {
    assert_eq!(tp_timeparse("2h32m"), Some(9120.0));
    assert_eq!(tp_timeparse("+2h32m"), Some(9120.0));
    assert_eq!(tp_timeparse("-2h32m"), Some(-9120.0));
}

#[test]
fn test_timeparse_3() {
    assert_eq!(tp_timeparse("3d2h32m"), Some(268320.0));
    assert_eq!(tp_timeparse("+3d2h32m"), Some(268320.0));
    assert_eq!(tp_timeparse("-3d2h32m"), Some(-268320.0));
}

#[test]
fn test_timeparse_4() {
    assert_eq!(tp_timeparse("1w3d2h32m"), Some(873120.0));
    assert_eq!(tp_timeparse("+1w3d2h32m"), Some(873120.0));
    assert_eq!(tp_timeparse("-1w3d2h32m"), Some(-873120.0));
}

#[test]
fn test_timeparse_5() {
    assert_eq!(tp_timeparse("1w 3d 2h 32m"), Some(873120.0));
    assert_eq!(tp_timeparse("+1w 3d 2h 32m"), Some(873120.0));
    assert_eq!(tp_timeparse("-1w 3d 2h 32m"), Some(-873120.0));
}

#[test]
fn test_timeparse_6() {
    assert_eq!(tp_timeparse("1 w 3 d 2 h 32 m"), Some(873120.0));
    assert_eq!(tp_timeparse("+1 w 3 d 2 h 32 m"), Some(873120.0));
    assert_eq!(tp_timeparse("-1 w 3 d 2 h 32 m"), Some(-873120.0));
}

#[test]
fn test_timeparse_7() {
    assert_eq!(tp_timeparse("4:13"), Some(253.0));
    assert_eq!(tp_timeparse("+4:13"), Some(253.0));
    assert_eq!(tp_timeparse("-4:13"), Some(-253.0));
}

#[test]
fn test_timeparse_bare_seconds() {
    assert_eq!(tp_timeparse(":13"), Some(13.0));
    assert_eq!(tp_timeparse("+:13"), Some(13.0));
    assert_eq!(tp_timeparse("-:13"), Some(-13.0));
}

#[test]
fn test_timeparse_8() {
    assert_eq!(tp_timeparse("4:13:02"), Some(15182.0));
    assert_eq!(tp_timeparse("+4:13:02"), Some(15182.0));
    assert_eq!(tp_timeparse("-4:13:02"), Some(-15182.0));
}

#[test]
fn test_timeparse_9() {
    assert_float_eq(tp_timeparse("4:13:02.266"), 15182.266);
    assert_float_eq(tp_timeparse("+4:13:02.266"), 15182.266);
    assert_float_eq(tp_timeparse("-4:13:02.266"), -15182.266);
}

#[test]
fn test_timeparse_10() {
    assert_float_eq(tp_timeparse("2:04:13:02.266"), 187982.266);
    assert_float_eq(tp_timeparse("+2:04:13:02.266"), 187982.266);
    assert_float_eq(tp_timeparse("-2:04:13:02.266"), -187982.266);
}

#[test]
fn test_timeparse_granularity_1() {
    // minute-level granularity
    use wroberts_pytimeparse::pytimeparse::timeparse::timeparse_with_granularity as tpg;
    assert_eq!(tpg("4:32", "minutes"), Some(272.0 * 60.0));
    assert_eq!(tpg("+4:32", "minutes"), Some(272.0 * 60.0));
    assert_eq!(tpg("-4:32", "minutes"), Some(-272.0 * 60.0));
}

#[test]
fn test_timeparse_granularity_2() {
    use wroberts_pytimeparse::pytimeparse::timeparse::timeparse_with_granularity as tpg;
    assert_eq!(tpg("4:32:02", "minutes"), Some(272.0 * 60.0 + 2.0));
    assert_eq!(tpg("+4:32:02", "minutes"), Some(272.0 * 60.0 + 2.0));
    assert_eq!(tpg("-4:32:02", "minutes"), Some(-(272.0 * 60.0 + 2.0)));
}

#[test]
fn test_timeparse_granularity_3() {
    use wroberts_pytimeparse::pytimeparse::timeparse::timeparse_with_granularity as tpg;
    assert_float_eq(tpg("7:02.223", "minutes"), 7.0 * 60.0 + 2.223);
    assert_float_eq(tpg("+7:02.223", "minutes"), 7.0 * 60.0 + 2.223);
    assert_float_eq(tpg("-7:02.223", "minutes"), -(7.0 * 60.0 + 2.223));
}

#[test]
fn test_timeparse_granularity_4() {
    use wroberts_pytimeparse::pytimeparse::timeparse::timeparse_with_granularity as tpg;
    assert_eq!(tpg("0:02", "seconds"), Some(2.0));
    assert_eq!(tpg("+0:02", "seconds"), Some(2.0));
    assert_eq!(tpg("-0:02", "seconds"), Some(-2.0));
}

#[test]
fn test_timeparse_11() {
    assert_eq!(tp_timeparse("2 days,  4:13:02"), Some(187982.0));
    assert_eq!(tp_timeparse("+2 days,  4:13:02"), Some(187982.0));
    assert_eq!(tp_timeparse("-2 days,  4:13:02"), Some(-187982.0));
}

#[test]
fn test_timeparse_12() {
    assert_float_eq(tp_timeparse("2 days,  4:13:02.266"), 187982.266);
    assert_float_eq(tp_timeparse("+2 days,  4:13:02.266"), 187982.266);
    assert_float_eq(tp_timeparse("-2 days,  4:13:02.266"), -187982.266);
}

#[test]
fn test_timeparse_13() {
    assert_eq!(tp_timeparse("5hr34m56s"), Some(20096.0));
    assert_eq!(tp_timeparse("+5hr34m56s"), Some(20096.0));
    assert_eq!(tp_timeparse("-5hr34m56s"), Some(-20096.0));
}

#[test]
fn test_timeparse_14() {
    assert_eq!(tp_timeparse("5 hours, 34 minutes, 56 seconds"), Some(20096.0));
    assert_eq!(tp_timeparse("+5 hours, 34 minutes, 56 seconds"), Some(20096.0));
    assert_eq!(tp_timeparse("-5 hours, 34 minutes, 56 seconds"), Some(-20096.0));
}

#[test]
fn test_timeparse_15() {
    assert_eq!(tp_timeparse("5 hrs, 34 mins, 56 secs"), Some(20096.0));
    assert_eq!(tp_timeparse("+5 hrs, 34 mins, 56 secs"), Some(20096.0));
    assert_eq!(tp_timeparse("-5 hrs, 34 mins, 56 secs"), Some(-20096.0));
}

#[test]
fn test_timeparse_16() {
    assert_eq!(tp_timeparse("2 days, 5 hours, 34 minutes, 56 seconds"), Some(192896.0));
    assert_eq!(tp_timeparse("+2 days, 5 hours, 34 minutes, 56 seconds"), Some(192896.0));
    assert_eq!(tp_timeparse("-2 days, 5 hours, 34 minutes, 56 seconds"), Some(-192896.0));
}

#[test]
fn test_timeparse_16b() {
    assert_float_eq(tp_timeparse("1.75 s"), 1.75);
    assert_float_eq(tp_timeparse("+1.75 s"), 1.75);
    assert_float_eq(tp_timeparse("-1.75 s"), -1.75);
}

#[test]
fn test_timeparse_16c() {
    assert_float_eq(tp_timeparse("1.75 sec"), 1.75);
    assert_float_eq(tp_timeparse("+1.75 sec"), 1.75);
    assert_float_eq(tp_timeparse("-1.75 sec"), -1.75);
}

#[test]
fn test_timeparse_16d() {
    assert_float_eq(tp_timeparse("1.75 secs"), 1.75);
    assert_float_eq(tp_timeparse("+1.75 secs"), 1.75);
    assert_float_eq(tp_timeparse("-1.75 secs"), -1.75);
}

#[test]
fn test_timeparse_16e() {
    assert_float_eq(tp_timeparse("1.75 second"), 1.75);
    assert_float_eq(tp_timeparse("+1.75 second"), 1.75);
    assert_float_eq(tp_timeparse("-1.75 second"), -1.75);
}

#[test]
fn test_timeparse_16f() {
    assert_float_eq(tp_timeparse("1.75 seconds"), 1.75);
    assert_float_eq(tp_timeparse("+1.75 seconds"), 1.75);
    assert_float_eq(tp_timeparse("-1.75 seconds"), -1.75);
}

#[test]
fn test_timeparse_17() {
    assert_eq!(tp_timeparse("1.2 m"), Some(72.0));
    assert_eq!(tp_timeparse("+1.2 m"), Some(72.0));
    assert_eq!(tp_timeparse("-1.2 m"), Some(-72.0));
}

#[test]
fn test_timeparse_18() {
    assert_eq!(tp_timeparse("1.2 min"), Some(72.0));
    assert_eq!(tp_timeparse("+1.2 min"), Some(72.0));
    assert_eq!(tp_timeparse("-1.2 min"), Some(-72.0));
}

#[test]
fn test_timeparse_19() {
    assert_eq!(tp_timeparse("1.2 mins"), Some(72.0));
    assert_eq!(tp_timeparse("+1.2 mins"), Some(72.0));
    assert_eq!(tp_timeparse("-1.2 mins"), Some(-72.0));
}

#[test]
fn test_timeparse_20() {
    assert_eq!(tp_timeparse("1.2 minute"), Some(72.0));
    assert_eq!(tp_timeparse("+1.2 minute"), Some(72.0));
    assert_eq!(tp_timeparse("-1.2 minute"), Some(-72.0));
}

#[test]
fn test_timeparse_21() {
    assert_eq!(tp_timeparse("1.2 minutes"), Some(72.0));
    assert_eq!(tp_timeparse("+1.2 minutes"), Some(72.0));
    assert_eq!(tp_timeparse("-1.2 minutes"), Some(-72.0));
}

#[test]
fn test_timeparse_22() {
    assert_eq!(tp_timeparse("172 hours"), Some(619200.0));
    assert_eq!(tp_timeparse("+172 hours"), Some(619200.0));
    assert_eq!(tp_timeparse("-172 hours"), Some(-619200.0));
}

#[test]
fn test_timeparse_23() {
    assert_eq!(tp_timeparse("172 hr"), Some(619200.0));
    assert_eq!(tp_timeparse("+172 hr"), Some(619200.0));
    assert_eq!(tp_timeparse("-172 hr"), Some(-619200.0));
}

#[test]
fn test_timeparse_24() {
    assert_eq!(tp_timeparse("172 h"), Some(619200.0));
    assert_eq!(tp_timeparse("+172 h"), Some(619200.0));
    assert_eq!(tp_timeparse("-172 h"), Some(-619200.0));
}

#[test]
fn test_timeparse_25() {
    assert_eq!(tp_timeparse("172 hrs"), Some(619200.0));
    assert_eq!(tp_timeparse("+172 hrs"), Some(619200.0));
    assert_eq!(tp_timeparse("-172 hrs"), Some(-619200.0));
}

#[test]
fn test_timeparse_26() {
    assert_eq!(tp_timeparse("172 hour"), Some(619200.0));
    assert_eq!(tp_timeparse("+172 hour"), Some(619200.0));
    assert_eq!(tp_timeparse("-172 hour"), Some(-619200.0));
}

#[test]
fn test_timeparse_27() {
    assert_eq!(tp_timeparse("1.24 days"), Some(107136.0));
    assert_eq!(tp_timeparse("+1.24 days"), Some(107136.0));
    assert_eq!(tp_timeparse("-1.24 days"), Some(-107136.0));
}

#[test]
fn test_timeparse_28() {
    assert_eq!(tp_timeparse("5 d"), Some(432000.0));
    assert_eq!(tp_timeparse("+5 d"), Some(432000.0));
    assert_eq!(tp_timeparse("-5 d"), Some(-432000.0));
}

#[test]
fn test_timeparse_29() {
    assert_eq!(tp_timeparse("5 day"), Some(432000.0));
    assert_eq!(tp_timeparse("+5 day"), Some(432000.0));
    assert_eq!(tp_timeparse("-5 day"), Some(-432000.0));
}

#[test]
fn test_timeparse_30() {
    assert_eq!(tp_timeparse("5 days"), Some(432000.0));
    assert_eq!(tp_timeparse("+5 days"), Some(432000.0));
    assert_eq!(tp_timeparse("-5 days"), Some(-432000.0));
}

#[test]
fn test_timeparse_31() {
    assert_eq!(tp_timeparse("5.6 wk"), Some(3386880.0));
    assert_eq!(tp_timeparse("+5.6 wk"), Some(3386880.0));
    assert_eq!(tp_timeparse("-5.6 wk"), Some(-3386880.0));
}

#[test]
fn test_timeparse_32() {
    assert_eq!(tp_timeparse("5.6 week"), Some(3386880.0));
    assert_eq!(tp_timeparse("+5.6 week"), Some(3386880.0));
    assert_eq!(tp_timeparse("-5.6 week"), Some(-3386880.0));
}

#[test]
fn test_timeparse_33() {
    assert_eq!(tp_timeparse("5.6 weeks"), Some(3386880.0));
    assert_eq!(tp_timeparse("+5.6 weeks"), Some(3386880.0));
    assert_eq!(tp_timeparse("-5.6 weeks"), Some(-3386880.0));
}

// Doctest skipped in Rust: not applicable.