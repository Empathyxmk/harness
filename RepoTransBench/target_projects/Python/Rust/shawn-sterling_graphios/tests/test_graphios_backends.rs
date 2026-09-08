use graphios_backends::*;

#[test]
fn test_load_backend_invalid() {
    let result = load_backend("doesnotexist", "", None);
    assert!(result.is_err());
}

#[test]
fn test_load_backend_file() {
    let backend = load_backend("file", "/tmp/testfile", None).expect("File backend should load");
    match backend {
        Backend::File(_) => {},
        _ => panic!("Expected FileBackend"),
    }
}

#[test]
fn test_load_backend_carbon() {
    let backend = load_backend("carbon", "host", Some(1234)).expect("Carbon backend should load");
    match backend {
        Backend::Carbon(_) => {},
        _ => panic!("Expected CarbonBackend"),
    }
}

#[test]
fn test_load_backend_udp() {
    let backend = load_backend("udp", "host", Some(1001)).expect("UDP backend should load");
    match backend {
        Backend::UDP(_) => {},
        _ => panic!("Expected UDPSendBackend"),
    }
}

#[test]
fn test_filebackend_send_metric() {
    use std::fs;
    let metric = FakeMetric {
        host: "a".to_string(),
        service: "b".to_string(),
        metric: "c".to_string(),
        value: "1".to_string(),
        timestamp: "2".to_string(),
    };
    let fpath = "test_filebackend_send_metric.txt";
    let back = FileBackend::new(fpath);
    back.send_metric(&metric);
    let data = fs::read_to_string(fpath).expect("file should exist");
    assert!(data.contains("a b c 1 2"), "file content: {}", data);
    fs::remove_file(fpath).unwrap();
}

#[test]
fn test_carbonbackend_send_metric() {
    let metric = FakeMetric {
        host: "h".to_string(),
        service: "s".to_string(),
        metric: "m".to_string(),
        value: "5".to_string(),
        timestamp: "18".to_string(),
    };
    let back = CarbonBackend::new("test.host", 2003);
    back.send_metric(&metric);
    let connected = back.connected.lock().unwrap().clone().unwrap();
    assert!(connected.contains("test.host"));
    let sent = back.sent.lock().unwrap().clone().unwrap();
    let data = String::from_utf8(sent).unwrap();
    assert!(data.contains("h.s.m 5 18"), "carbon sent data: {}", data);
}

#[test]
fn test_udpbackend_send_metric() {
    let metric = FakeMetric {
        host: "hosty".to_string(),
        service: "svc".to_string(),
        metric: "metric".to_string(),
        value: "3".to_string(),
        timestamp: "6".to_string(),
    };
    let back = UDPSendBackend::new("testhost", 2222);
    back.send_metric(&metric);
    let sent = back.sent.lock().unwrap().clone().unwrap();
    let (_data, addr) = sent;
    assert!(addr.contains("testhost:2222"));
}