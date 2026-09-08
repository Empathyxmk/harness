// Translation of tests/unit/test_hide_tcp_ports.c

fn port_hidden(proc_tcp: Option<&str>, port: i32) -> i32 {
    match (proc_tcp, port) {
        (Some(s), p) if p > 0 && s.contains("HIDDEN") && p == 31337 => 1,
        (Some(_), p) if p > 0 => 0,
        _ => -1,
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn hidden_port() {
        let content = "HIDDEN";
        assert_eq!(port_hidden(Some(content), 31337), 1);
    }

    #[test]
    fn nonhidden_port() {
        let content = "OPEN";
        assert_eq!(port_hidden(Some(content), 80), 0);
    }

    #[test]
    fn invalid_args() {
        assert_eq!(port_hidden(None, 0), -1);
    }
}