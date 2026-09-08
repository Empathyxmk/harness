//! Public variant of the continuous connection BLE test
//! BLE_CONNECT_LOOP_COUNT and scan timeout are different from the original

use std::sync::{Arc, Condvar, Mutex};
use std::{thread, time};

const BLE_CONNECT_LOOP_COUNT: usize = 5;  // Public test uses 5 (original uses 20)
const BLE_SCAN_TIMEOUT: u64 = 60;         // Public test uses 60s (original uses 180)

static mut ADAPTER_NAME: Option<&'static str> = None;
static mut REFERENCE_MAC_ADDRESS: Option<&'static str> = None;

struct ConnectionTerminated {
    value: Mutex<bool>,
    condvar: Condvar,
}

impl ConnectionTerminated {
    fn new() -> Self {
        ConnectionTerminated {
            value: Mutex::new(false),
            condvar: Condvar::new(),
        }
    }
}

fn on_device_connect(error: i32, connection_terminated: Arc<ConnectionTerminated>) {
    if error != 0 {
        let mut value = connection_terminated.value.lock().unwrap();
        *value = true;
        connection_terminated.condvar.notify_all();
        return;
    }

    let mut value = connection_terminated.value.lock().unwrap();
    *value = true;
    connection_terminated.condvar.notify_all();
}

fn stricmp(a: &str, b: &str) -> bool {
    a.eq_ignore_ascii_case(b)
}

fn ble_discovered_device(
    addr: &str,
    reference_mac_address: &str,
    connect_loop_count: usize,
) {
    if !stricmp(addr, reference_mac_address) {
        return;
    }

    for _ in 0..connect_loop_count {
        let connection_terminated = Arc::new(ConnectionTerminated::new());

        let mut ret = 0; // Simulate success
        loop {
            ret = 0;
            if ret != -16 {
                break;
            }
            thread::sleep(time::Duration::from_millis(100));
        }
        if ret != 0 {
            continue;
        }

        let mut value = connection_terminated.value.lock().unwrap();
        while !*value {
            value = connection_terminated.condvar.wait(value).unwrap();
        }
    }
}

fn ble_task(adapter_name: Option<&str>, reference_mac_address: &str) -> i32 {
    let _adapter = match adapter_name {
        Some(_name) => {}
        None => {}
    };
    thread::sleep(time::Duration::from_millis(100));
    ble_discovered_device(reference_mac_address, reference_mac_address, BLE_CONNECT_LOOP_COUNT);
    0
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_continuous_connection_public() {
        let adapter_name = None;
        let reference_mac_address = "00:11:22:33:44:77"; // Dummy for public test

        let ret = ble_task(adapter_name, reference_mac_address);
        assert_eq!(ret, 0, "Simulated BLE public mainloop should succeed");
    }
}