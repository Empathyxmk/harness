use serde_json::Value;
use std::collections::HashMap;
use std::env;

#[derive(Default)]
struct DummyContainer {
    // Simulates relevant state from the original DummyContainer
    top: Option<serde_json::Map<String, Value>>,
    exec_run_out: Option<String>,
    logs_bytes: Option<Vec<u8>>,
    has_gunicorn: bool,
    raise_on_top: bool,
    raise_on_exec_run: bool,
    stop_called: bool,
    remove_called: bool,
}

impl DummyContainer {
    fn new(
        top: Option<serde_json::Map<String, Value>>,
        exec_run_out: Option<String>,
        logs_bytes: Option<Vec<u8>>,
        has_gunicorn: bool,
        raise_on_top: bool,
        raise_on_exec_run: bool,
    ) -> Self {
        let default_top = if has_gunicorn {
            serde_json::json!({"Processes": [[
                "a","b","c","d","e","f","g","gunicorn -c conf.py app:app"
            ]]}).as_object().unwrap().clone()
        } else {
            serde_json::json!({"Processes": [[
                "a","b","c","d","e","f","g","python app.py"
            ]]}).as_object().unwrap().clone()
        };
        DummyContainer {
            top: top.or(Some(default_top)),
            exec_run_out: exec_run_out.or(Some("{\"key\": \"value\"}".to_string())),
            logs_bytes: logs_bytes.or(Some(b"Some logs".to_vec())),
            has_gunicorn,
            raise_on_top,
            raise_on_exec_run,
            stop_called: false,
            remove_called: false,
        }
    }

    fn top(&mut self) -> Result<serde_json::Map<String, Value>, &'static str> {
        if self.raise_on_top {
            return Err("Cannot get top of container");
        }
        Ok(self.top.clone().unwrap())
    }

    fn exec_run(&mut self, _cmd: &str) -> Result<String, &'static str> {
        if self.raise_on_exec_run {
            return Err("exec_run failed");
        }
        Ok(self.exec_run_out.clone().unwrap())
    }

    fn logs(&mut self) -> Vec<u8> {
        self.logs_bytes.clone().unwrap()
    }

    fn stop(&mut self) {
        self.stop_called = true;
    }

    fn remove(&mut self) {
        self.remove_called = true;
    }
}

struct DummyClient {
    container: Option<DummyContainer>,
    notfound: bool,
}

impl DummyClient {
    fn new(container: Option<DummyContainer>, notfound: bool) -> Self {
        Self { container, notfound }
    }

    fn get_container(&mut self, _name: &str) -> Result<&mut DummyContainer, &'static str> {
        if self.notfound {
            return Err("not found");
        }
        match self.container.as_mut() {
            Some(c) => Ok(c),
            None => Err("not found (no container)"),
        }
    }
}

// --- Helper functions simulating 'utils' module in Python ---

fn get_process_names(container: &mut DummyContainer) -> Vec<String> {
    let top = container.top().unwrap();
    let procs = top
        .get("Processes")
        .and_then(|val| val.as_array())
        .cloned()
        .unwrap_or_else(Vec::new);
    procs
        .into_iter()
        .flat_map(|proc| {
            proc.as_array().unwrap().iter().map(|x| x.as_str().unwrap().to_string())
        })
        .filter(|cmd| cmd.contains("gunicorn"))
        .collect()
}

fn get_gunicorn_conf_path(container: &mut DummyContainer) -> String {
    let top = container.top().unwrap();
    let procs = top.get("Processes").unwrap().as_array().unwrap();
    for proc_row in procs {
        for part in proc_row.as_array().unwrap() {
            let line = part.as_str().unwrap();
            if let Some(idx) = line.find("gunicorn") {
                for w in line.split_whitespace() {
                    if w == "-c" {
                        let pos = line.split_whitespace().position(|w2| w2 == "-c").unwrap();
                        // return next word after -c
                        let words: Vec<&str> = line.split_whitespace().collect();
                        return words.get(pos + 1).unwrap().to_string();
                    }
                }
            }
        }
    }
    panic!("No gunicorn conf found");
}

fn get_config(container: &mut DummyContainer) -> HashMap<String, serde_json::Value> {
    let out = container.exec_run("cat config").unwrap();
    let v: serde_json::Value = serde_json::from_str(&out).unwrap();
    v.as_object().unwrap().clone()
}

fn remove_previous_container(client: &mut DummyClient) -> Option<()> {
    let c_result = client.get_container("random");
    match c_result {
        Ok(c) => {
            c.stop();
            c.remove();
            Some(())
        }
        Err(_) => None,
    }
}

fn get_logs(container: &mut DummyContainer) -> String {
    let bytes = container.logs();
    match String::from_utf8(bytes) {
        Ok(s) => s,
        Err(e) => panic!("{}", e),
    }
}

fn get_response_text1() -> String {
    let python_ver = env::var("PYTHON_VERSION").unwrap_or("unknown".into());
    format!("Some response with Python {python_ver}")
}

// =============== TESTS =============== //

#[test]
fn test_get_process_names() {
    let mut c = DummyContainer::new(None, None, None, true, false, false);
    let res = get_process_names(&mut c);
    assert!(res.iter().any(|x| x == "gunicorn -c conf.py app:app"));
}

#[test]
fn test_get_process_names_empty() {
    let mut c = DummyContainer::new(None, None, None, false, false, false);
    let res = get_process_names(&mut c);
    assert!(res.is_empty());
}

#[test]
fn test_get_gunicorn_conf_path() {
    let mut c = DummyContainer::new(None, None, None, true, false, false);
    let path = get_gunicorn_conf_path(&mut c);
    assert_eq!(path, "conf.py");
}

#[test]
#[should_panic]
fn test_get_gunicorn_conf_path_no_gunicorn() {
    let mut c = DummyContainer::new(None, None, None, false, false, false);
    get_gunicorn_conf_path(&mut c);
}

#[test]
fn test_get_config() {
    let mut c = DummyContainer::new(
        None,
        Some("{\"foo\":42}".to_string()),
        None,
        true,
        false,
        false,
    );
    let config = get_config(&mut c);
    assert_eq!(config.get("foo").unwrap(), &serde_json::json!(42));
}

#[test]
#[should_panic]
fn test_get_config_exec_run_error() {
    let mut c = DummyContainer::new(None, None, None, true, false, true);
    get_config(&mut c);
}

#[test]
fn test_remove_previous_container_found() {
    let mut c = DummyContainer::new(None, None, None, true, false, false);
    let mut client = DummyClient::new(Some(c), false);
    let _ = remove_previous_container(&mut client);
    let c_mut = client.container.as_ref().unwrap();
    assert!(c_mut.stop_called);
    assert!(c_mut.remove_called);
}

#[test]
fn test_remove_previous_container_notfound() {
    let mut client = DummyClient::new(None, true);
    let res = remove_previous_container(&mut client);
    assert!(res.is_none());
}

#[test]
fn test_get_logs() {
    let mut c =
        DummyContainer::new(None, None, Some(b"abc123".to_vec()), true, false, false);
    let logs = get_logs(&mut c);
    assert_eq!(logs, "abc123".to_string());
}

#[test]
fn test_get_response_text1() {
    env::set_var("PYTHON_VERSION", "3.9");
    let msg = get_response_text1();
    assert!(msg.contains("3.9"));
}

#[test]
#[should_panic]
fn test_get_logs_utf8_error() {
    struct Container;
    impl Container {
        fn logs(&self) -> Vec<u8> {
            vec![0xff]
        }
    }
    // Use a struct compatible with interface
    let bytes = Container {}.logs();
    String::from_utf8(bytes).unwrap();
}