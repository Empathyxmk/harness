// Translation of shortuuid/test_cli_argparse_errors.py

#[cfg(test)]
mod tests {
    use std::process::Command;
    use std::str;

    #[test]
    fn test_cli_fails_with_invalid_arg() {
        let output = Command::new("cargo")
            .args(&["run", "--", "--notarealflag"])
            .output()
            .expect("failed to execute process");
        let stdout = str::from_utf8(&output.stdout).unwrap();
        let stderr = str::from_utf8(&output.stderr).unwrap();
        // Should indicate unrecognized or unknown argument
        let needle = "error" ;
        let found = stdout.to_lowercase().contains(needle) || stderr.to_lowercase().contains(needle);
        assert!(
            found,
            "Should print error for invalid argument. Stdout: {} Stderr: {}",
            stdout,
            stderr
        );
        // Exit code typically non-zero on argparse errors
        assert_ne!(output.status.code().unwrap_or(0), 0);
    }
}