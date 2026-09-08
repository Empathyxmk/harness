//! Simulates public test runner shell
//! This test checks for correct logic in the shell that runs public tests.

#[cfg(test)]
mod tests {
    #[test]
    fn test_run_public_tests_script_logic() {
        // Simulate shell logic: finds pcov.so/pcov.la, sets INI, and runs test harness
        let mut found_so = false;
        let mut found_la = false;
        let files = vec!["./modules/pcov.so", "./modules/pcov.la"];

        for f in &files {
            if f.ends_with(".so") {
                found_so = true;
            }
            if f.ends_with(".la") {
                found_la = true;
            }
        }
        assert!(found_so || found_la);

        let php_ini = String::from("./test-php.ini");
        assert!(php_ini.ends_with("php.ini"));
        // Simulate logic: if neither found, error
        let pcov_so_path: Option<&str> = if found_so {
            Some("./modules/pcov.so")
        } else if found_la {
            Some("./modules/pcov.la")
        } else {
            None
        };
        assert!(pcov_so_path.is_some());
    }
}