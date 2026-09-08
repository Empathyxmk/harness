use crate::export::systemd::*;

use std::collections::HashMap;

#[test]
fn test_systemd_get_master_target_name_public() {
    assert_eq!(get_master_target_name("foobar"), "foobar-master.target");
    assert_eq!(get_master_target_name("qwerty"), "qwerty-master.target");
}

#[test]
fn test_systemd_get_service_name_public() {
    assert_eq!(get_service_name("myapp", "api", 5), "myapp-api-5.service");
    assert_eq!(get_service_name("weather", "web", 2), "weather-web-2.service");
}

#[test]
fn test_systemd_get_service_and_master_target_public() {
    let mut procs = HashMap::new();
    procs.insert("worker", "python app.py");
    let conc = Some(HashMap::from([("worker", 2)]));
    let files = get_service_and_master_target("foo", &procs, conc);
    let file_names: Vec<_> = files.iter().map(|f| f.name.clone()).collect();
    assert!(file_names.contains(&"foo-master.target".to_string()));
    assert!(file_names.contains(&"foo-worker-1.service".to_string()));
    assert!(file_names.contains(&"foo-worker-2.service".to_string()));
}