use serde_json::{Map, Value};
use std::collections::HashMap;

struct DummyContainer {
    top: Map<String, Value>,
    exec_run_out: String,
    logs_bytes: Vec<u8>,
    raise_on_top: bool,
    raise_on_exec_run: bool,
    stop_called: bool,
    remove_called: bool,
}

impl DummyContainer {
    fn new(
        logs_bytes: Option<Vec<u8>>,
        raise_on_top: bool,
        raise_on_exec_run: bool,
    ) -> Self {
        DummyContainer {
            top: serde_json::json!({"Processes": [[
                "a","b","c","d","e","f","g", "gunicorn -c conf.py app:app"
            ]]}).as_object().unwrap().clone(),
            exec_run_out: "{\"newkey\": \"newvalue\"}".to_string(),
            logs_bytes: logs_bytes.unwrap_or_else(|| b"logdata".to_vec()),
            raise_on_top,
            raise_on_exec_run,
            stop_called: false,
            remove_called: false,
        }
    }

    fn top(&mut self) -> Result<Map<String, Value>, &'static str> {
        if self.raise_on_top {
            return Err("Simulate top error");
        }
        Ok(self.top.clone())
    }

    fn exec_run(&mut self, _cmd: &str) -> Result<String, &'static str> {
        if self.raise_on_exec_run {
            return Err("Simulate exec_run error");
        }
        Ok(self.exec_run_out.clone())
    }

    fn logs(&mut self) -> Vec<u8> {
        self.logs_bytes.clone()
    }

    fn stop(&mut self) {
        self.stop_called = true;
    }

    fn remove(&mut self) {
        self.remove_called = true;
    }
}

fn wait_for_gunicorn(
    c: &mut DummyContainer,
    _sleep_time: f64,
    _timeout: f64,
) -> bool {
    match c.top() {
        Ok(top) => {
            let procs = top.get("Processes").unwrap().as_array().unwrap();
            for proc_row in procs {
                let proc_vec = proc_row.as_array().unwrap();
                for item in proc_vec {
                    if item.as_str().unwrap().contains("gunicorn") {
                        return true;
                    }
                }
            }
        }
        Err(_) => {}
    }
    false
}

fn get_config_from_container(
    c: &mut DummyContainer,
    _path: &str,
) -> Option<HashMap<String, Value>> {
    match c.exec_run("cat something") {
        Ok(s) => {
            let v: Value = serde_json::from_str(&s).unwrap();
            Some(v.as_object().unwrap().clone())
        }
        Err(_) => None,
    }
}

fn print_container_logs(c: &mut DummyContainer) {
    let logs = String::from_utf8_lossy(&c.logs());
    println!("Container logs: {}", logs);
}

fn cleanup_container(c: &mut DummyContainer) {
    c.stop();
    c.remove();
}

#[test]
fn test_wait_for_gunicorn_gunicorn_found() {
    let mut c = DummyContainer::new(None, false, false);
    let result = wait_for_gunicorn(&mut c, 0.01, 0.05);
    assert!(result);
}

#[test]
fn test_wait_for_gunicorn_gunicorn_notfound() {
    let mut c = DummyContainer::new(None, false, false);
    c.top = serde_json::json!({"Processes": [[ "python app.py" ]]}).as_object().unwrap().clone();
    let result = wait_for_gunicorn(&mut c, 0.01, 0.03);
    assert!(!result);
}

#[test]
fn test_get_config_from_container_success() {
    let mut c = DummyContainer::new(None, false, false);
    let r = get_config_from_container(&mut c, "/etc/config.json");
    assert!(r.unwrap().contains_key("newkey"));
}

#[test]
fn test_get_config_from_container_exec_run_fail() {
    let mut c = DummyContainer::new(None, false, true);
    let r = get_config_from_container(&mut c, "/fakepath");
    assert!(r.is_none());
}

#[test]
fn test_print_container_logs_prints() {
    let mut c = DummyContainer::new(None, false, false);
    print_container_logs(&mut c);
}

#[test]
fn test_cleanup_container_calls_methods() {
    let mut c = DummyContainer::new(None, false, false);
    cleanup_container(&mut c);
    assert!(c.stop_called);
    assert!(c.remove_called);
}