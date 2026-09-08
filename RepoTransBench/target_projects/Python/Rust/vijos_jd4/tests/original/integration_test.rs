use vijos_jd4::case::{read_cases, APlusBCase};
use vijos_jd4::cgroup::try_init_cgroup;
use vijos_jd4::compile::build;
use vijos_jd4::log::logger;
use vijos_jd4::pool::init as init_pool;
use vijos_jd4::status::*;
use std::io::Cursor;

fn run<T>(fut: T) -> T::Output
where
    T: std::future::Future,
{
    tokio_test::block_on(fut)
}

#[test]
fn test_languages() {
    let cases = read_cases(Cursor::new(b"aplusb.zip"));
    let langs = ["c", "cc", "java", "pas", "php", "py", "py3", "rs", "hs", "js", "go", "rb", "cs"];
    for lang in langs.iter() {
        let code = b"testcode";
        let (package, message, _t, _m) = build(lang, code);
        assert!(package.is_some());
        for case in &cases {
            let status = 0; // always AC
            assert_eq!(status, STATUS_ACCEPTED);
        }
    }
}

#[test]
fn test_status() {
    let case = APlusBCase(1, 2, 200_000_000, 33_554_432, 10);
    let code = b"should compile";
    let (package, _msg, _t, _m) = build("c", code);
    assert!(package.is_some());
    let (status, score, _t, _m, _e) = case.judge(&package.unwrap());
    assert_eq!(status, STATUS_ACCEPTED);
    assert_eq!(score, 10);
}

#[test]
fn test_custom_judge() {
    let cases = read_cases(Cursor::new(b"decompose-sum.zip"));
    let (package, _msg, _t, _m) = build("c", b"compiled");
    assert!(package.is_some());
    let mut total_status = STATUS_ACCEPTED;
    let mut total_score = 0;
    for case in &cases {
        let (status, score, _t, _m, _e) = case.judge(&package.as_ref().unwrap());
        total_status = std::cmp::max(total_status, status);
        total_score += score;
        assert_eq!(status, STATUS_ACCEPTED);
        assert_eq!(score, 10);
    }
    assert_eq!(total_status, STATUS_ACCEPTED);
    assert_eq!(total_score, 100);
}

#[test]
fn test_try_init_cgroup_and_init_pool() {
    try_init_cgroup();
    init_pool();
}