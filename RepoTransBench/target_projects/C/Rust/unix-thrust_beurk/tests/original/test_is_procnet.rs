// Translation of tests/unit/test_is_procnet.c

fn is_procnet(path: Option<&str>) -> i32 {
    match path {
        None => 0,
        Some(s) => {
            if s.contains("/proc/net/") { 1 } else { 0 }
        }
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn procnet_tcp() {
        assert_eq!(is_procnet(Some("/proc/net/tcp")), 1);
    }

    #[test]
    fn procnet_udp() {
        assert_eq!(is_procnet(Some("/proc/net/udp")), 1);
    }

    #[test]
    fn not_procnet() {
        assert_eq!(is_procnet(Some("/etc/passwd")), 0);
    }

    #[test]
    fn null_arg() {
        assert_eq!(is_procnet(None), 0);
    }
}