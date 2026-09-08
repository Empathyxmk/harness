// Translation of tests/unit/test_cleanup_login_records.c

fn cleanup_login_records(filename: Option<&str>) -> i32 {
    match filename {
        None => -1,
        Some(s) if s.starts_with('/') => 1,
        Some(_) => 0,
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn null_filename() {
        assert_eq!(cleanup_login_records(None), -1);
    }

    #[test]
    fn absolute_path() {
        assert_eq!(cleanup_login_records(Some("/var/log/utmp")), 1);
    }

    #[test]
    fn rel_path() {
        assert_eq!(cleanup_login_records(Some("utmp")), 0);
    }
}