// Translation of tests/unit/test_is_procnet_public.c

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
    fn procnet_unix() {
        assert_eq!(is_procnet(Some("/proc/net/unix")), 1);
    }

    #[test]
    fn procnet_raw() {
        assert_eq!(is_procnet(Some("/proc/net/raw")), 1);
    }

    #[test]
    fn not_procnet_var() {
        assert_eq!(is_procnet(Some("/var/log/syslog")), 0);
    }

    #[test]
    fn empty_string() {
        assert_eq!(is_procnet(Some("")), 0);
    }
}