use graphios::*;
use std::collections::HashMap;

#[test]
fn test_public_create_metric_line() {
    let line = create_metric_line(
        "disk_usage", "server3", "DiskIO", "write", 0.99, 456, 678, "2024-02-10 08:00:00"
    );
    assert_eq!(line, "disk_usage,server3,DiskIO,write,0.99,456,678,2024-02-10 08:00:00");
}

#[test]
fn test_public_parse_value() {
    match parse_value("52.34") {
        Ok(v) => assert_eq!(v, 52.34),
        Err(_) => panic!("parse_value did not parse float"),
    }
    match parse_value("off") {
        Ok(_) => panic!("Should return Err for non-float"),
        Err(v) => assert_eq!(v, "off"),
    }
}

#[test]
fn test_public_format_perfdata() {
    let mut pd = HashMap::new();
    pd.insert("label", serde_json::json!("free_mem"));
    pd.insert("value", serde_json::json!(1234));
    pd.insert("uom", serde_json::json!("MB"));
    pd.insert("warn", serde_json::json!(""));
    pd.insert("crit", serde_json::json!(""));
    pd.insert("min", serde_json::json!(128));
    pd.insert("max", serde_json::json!(4096));
    let result = format_perfdata(&pd);
    assert!(result.starts_with("'free_mem'=1234MB;;;128;4096"), "perfdata format failed: {}", result);
}

#[test]
fn test_public_split_perfdata() {
    let perfdata = "'cpu'=15%;20;30;0;100 'mem'=4096MB;;;128;16384";
    let pd_list = split_perfdata(perfdata);
    assert_eq!(pd_list[1]["label"], "mem");
    assert_eq!(pd_list[1]["value"], 4096.into());
    assert_eq!(pd_list[1]["uom"], "MB");
}

#[test]
fn test_public_strip_perf_label() {
    assert_eq!(strip_perf_label("'swap'"), "swap");
    assert_eq!(strip_perf_label("disk"), "disk");
}

#[test]
fn test_public_is_numeric() {
    assert!(is_numeric("483.3"));
    assert!(!is_numeric("test998"));
}

#[test]
fn test_public_perfdata2list() {
    let pd = "'io_read'=1MB 'io_write'=2MB;;;0;100";
    let res = perfdata2list(pd);
    assert_eq!(res[0]["label"], "io_read");
    assert_eq!(res[1]["label"], "io_write");
}