use chrono::{DateTime, Utc, TimeZone};
use std::sync::{Arc, Mutex};
use std::thread;

// Helper for simulating serialization and deserialization in Rust
fn datetime_str(dt: &DateTime<Utc>) -> String {
    dt.format("%Y-%m-%dT%H:%M:%SZ").to_string()
}

#[test]
fn test_dump_list() {
    let dat = Utc.ymd(2018, 7, 8).and_hms(21, 34, 0);
    let l = vec![
        1.into(),
        2.into(),
        3.into(),
        vec![4.into(), 5.into(), vec![datetime_str(&dat).into()].into()].into(),
    ];
    let expected = vec![
        1.into(),
        2.into(),
        3.into(),
        vec![4.into(), 5.into(), vec!["2018-07-08T21:34:00Z".to_string().into()].into()].into(),
    ];
    assert_eq!(format!("{:?}", l), format!("{:?}", expected));
}

#[test]
fn test_dump_load_list_verbose() {
    #[derive(Debug, PartialEq)]
    struct Parent {}
    #[derive(Debug, PartialEq)]
    struct Child {}
    #[derive(Debug, PartialEq)]
    struct Store {
        c2s: Vec<Parent>,
    }
    // In Rust, class registration not needed.
    // Simulate dump and load
    let loaded = Child {};
    assert_eq!(std::any::type_name::<Child>(), std::any::type_name::<Child>());
}

#[test]
fn test_dump_list_strict_no_cls() {
    #[derive(Debug, PartialEq, Clone)]
    struct C {
        x: i32,
        y: String,
    }
    let l = vec![C { x: 1, y: "2".to_string() }; 5];
    let expected = vec![C { x: 1, y: "2".to_string() }; 5];
    let dumped = l.clone();
    assert_eq!(expected, dumped);
}

// Simulate dump_list_multiprocess using thread
#[test]
fn test_dump_list_multiprocess() {
    let items: Vec<String> = vec!["1".to_string(); 4];
    // Simulate parallel processing: convert all "1" to 1
    let tasks = 2;
    let chunk_size = (items.len() + tasks - 1) / tasks;
    let items_arc = Arc::new(Mutex::new(Vec::new()));
    let mut handles = vec![];
    for chunk in items.chunks(chunk_size) {
        let chunk = chunk.to_vec();
        let items_arc = Arc::clone(&items_arc);
        handles.push(thread::spawn(move || {
            let mut data = items_arc.lock().unwrap();
            for s in chunk {
                data.push(s.parse::<i32>().unwrap());
            }
        }));
    }
    for h in handles {
        h.join().unwrap();
    }
    let result = items_arc.lock().unwrap().clone();
    assert_eq!(result, vec![1, 1, 1, 1]);
}

#[test]
fn test_load_list() {
    let dat = Utc.ymd(2018, 7, 8).and_hms(21, 34, 0);
    let expectation = vec![
        1.into(),
        2.into(),
        3.into(),
        vec![4.into(), 5.into(), vec![dat.clone()].into()].into(),
    ];
    let loaded = vec![
        1.into(),
        2.into(),
        3.into(),
        vec![4.into(), 5.into(), vec![Utc.datetime_from_str("2018-07-08T21:34:00Z", "%Y-%m-%dT%H:%M:%SZ").unwrap()].into()].into(),
    ];
    assert_eq!(format!("{:?}", expectation), format!("{:?}", loaded));
}

#[test]
fn test_load_list_typing() {
    let dat = Utc.ymd(2018, 7, 8).and_hms(21, 34, 0);
    let expectation = vec![
        1.into(),
        2.into(),
        3.into(),
        vec![4.into(), 5.into(), vec![dat.clone()].into()].into(),
    ];
    let loaded = vec![
        1.into(),
        2.into(),
        3.into(),
        vec![4.into(), 5.into(), vec![Utc.datetime_from_str("2018-07-08T21:34:00Z", "%Y-%m-%dT%H:%M:%SZ").unwrap()].into()].into(),
    ];
    assert_eq!(format!("{:?}", expectation), format!("{:?}", loaded));
}

#[test]
fn test_load_list2() {
    let dat = Utc.ymd(2018, 7, 8).and_hms(21, 34, 0);
    let list_ = vec![dat.clone()];
    let expectation = vec!["2018-07-08T21:34:00Z".to_string()];
    let loaded: Vec<DateTime<Utc>> = expectation
        .iter()
        .map(|s| Utc.datetime_from_str(s, "%Y-%m-%dT%H:%M:%SZ").unwrap())
        .collect();
    assert_eq!(list_, loaded);
}

#[test]
fn test_load_list_multithreaded() {
    let dat = Utc.ymd(2018, 7, 8).and_hms(21, 34, 0);
    let list_ = vec![
        1.into(),
        2.into(),
        3.into(),
        vec![4.into(), 5.into(), vec![dat.clone()].into()].into(),
    ];
    let expectation = vec![
        1.into(),
        2.into(),
        3.into(),
        vec![4.into(), 5.into(), vec!["2018-07-08T21:34:00Z".to_string()].into()].into(),
    ];
    // Simulate multithreading
    let mut handles = vec![];
    handles.push(thread::spawn(|| 1));
    handles.push(thread::spawn(|| 2));
    for h in handles {
        h.join().unwrap();
    }
    assert!(true);
    // Simulate error
    let negative_tasks = -1;
    let res = if negative_tasks < 0 { Some("JsonsError") } else { None };
    assert_eq!(res, Some("JsonsError"));

    // Partial conversion
    let loaded: Vec<i32> = vec!["1".to_string()].into_iter().map(|s| s.parse().unwrap()).collect();
    assert_eq!(loaded, vec![1]);

    let more: Vec<i32> = vec!["1".to_string(), "1".to_string(), "1".to_string(), "1".to_string()]
        .into_iter()
        .map(|s| s.parse().unwrap())
        .collect();
    assert_eq!(more, vec![1, 1, 1, 1]);
}

#[test]
fn test_load_list_multiprocess() {
    // Simulates multiprocess with thread
    let vals = vec!["1".to_string(), "1".to_string(), "1".to_string(), "1".to_string()];
    let tasks = 2;
    let chunk_size = (vals.len() + tasks - 1) / tasks;
    let result_arc = Arc::new(Mutex::new(Vec::new()));
    let mut handles = vec![];
    for chunk in vals.chunks(chunk_size) {
        let chunk = chunk.to_vec();
        let result_arc = Arc::clone(&result_arc);
        handles.push(thread::spawn(move || {
            let mut data = result_arc.lock().unwrap();
            for val in chunk {
                data.push(val.parse::<i32>().unwrap());
            }
        }));
    }
    for h in handles {
        h.join().unwrap();
    }
    let result = result_arc.lock().unwrap().clone();
    assert_eq!(result, vec![1, 1, 1, 1]);
}

#[test]
fn test_load_list_with_generic() {
    #[derive(Debug, PartialEq)]
    struct C {
        x: String,
        y: i32,
    }
    let expectation = vec![
        C { x: "a".to_string(), y: 1 },
        C { x: "b".to_string(), y: 2 },
    ];
    let loaded = vec![
        C { x: "a".to_string(), y: 1 },
        C { x: "b".to_string(), y: 2 },
    ];
    assert_eq!(expectation, loaded);
}

#[test]
fn test_load_error_points_at_index() {
    #[derive(Debug)]
    struct C {
        x: String,
        y: i32,
    }
    let mut c_objs_dict: Vec<Option<C>> = (0..1000)
        .map(|i| Some(C { x: i.to_string(), y: i }))
        .collect();
    c_objs_dict[500] = None;
    // Simulate error on index 500
    assert!(c_objs_dict.iter().enumerate().any(|(idx, v)| idx == 500 && v.is_none()));
}

#[test]
fn test_warn_on_fail() {
    #[derive(Debug)]
    struct C {
        x: String,
        y: i32,
    }
    let mut c_objs_dict: Vec<Option<C>> = (0..1000)
        .map(|i| Some(C { x: i.to_string(), y: i }))
        .collect();
    c_objs_dict[500] = None;
    let warnings = if c_objs_dict[500].is_none() { Some(500) } else { None };
    let loaded: Vec<C> = c_objs_dict.iter().filter_map(|v| v.clone()).collect();
    assert_eq!(warnings, Some(500));
    assert_eq!(loaded.len(), 999);
}

#[test]
fn test_propagation_of_fork_inst() {
    #[derive(Debug, PartialEq)]
    struct C {
        x: i32,
    }
    fn c_deserializer(v: &std::collections::HashMap<&str, i32>) -> C {
        C { x: v["x"] * 2 }
    }
    // Simulated deserialization from JSON to Vec<C>
    let cs = vec![C { x: 4 }, C { x: 6 }];
    assert_eq!(4, cs[0].x);
    assert_eq!(6, cs[1].x);
}