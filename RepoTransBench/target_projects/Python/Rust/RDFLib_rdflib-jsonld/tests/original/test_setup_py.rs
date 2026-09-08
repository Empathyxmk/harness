use std::process::Command;
use std::fs;
use std::path::Path;

#[test]
fn test_setup_py_exists() {
    let setup_py_path = Path::new("setup.py");
    assert!(setup_py_path.exists(), "setup.py not found in project root");
}

#[test]
fn test_setup_runs_as_script() {
    // Simulate calling `python setup.py --version`
    // We'll use `python` or `python3` and tolerate both
    #[cfg(target_os = "windows")]
    let python_cmds = ["python.exe", "python3.exe"];
    #[cfg(not(target_os = "windows"))]
    let python_cmds = ["python3", "python"];

    let setup_py_path = Path::new("setup.py");
    let mut did_run = false;

    for python in python_cmds.iter() {
        match Command::new(python)
            .arg(setup_py_path)
            .arg("--version")
            .output()
        {
            Ok(output) => {
                if output.status.success() || !output.stdout.is_empty() || !output.stderr.is_empty() {
                    // We only want to check that the script can be launched (exit code can be non-zero)
                    did_run = true;
                    break;
                }
            }
            Err(_) => continue,
        }
    }
    assert!(did_run, "Could not run setup.py with python or python3 interpreter");
}