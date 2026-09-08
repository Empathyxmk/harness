// Translation of tests/unit/test_drop_shell_backdoor.c

fn drop_shell_backdoor(cmd: Option<&str>) -> i32 {
    match cmd {
        None => -1,
        Some("evil") => 1,
        Some(_) => 0,
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn drop_null_cmd() {
        assert_eq!(drop_shell_backdoor(None), -1);
    }

    #[test]
    fn drop_evil_cmd() {
        assert_eq!(drop_shell_backdoor(Some("evil")), 1);
    }

    #[test]
    fn drop_benign_cmd() {
        assert_eq!(drop_shell_backdoor(Some("benign")), 0);
    }
}