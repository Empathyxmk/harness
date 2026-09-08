use std::fs;
use std::process::Command;
use std::path::Path;

#[test]
fn test_setup_runs_with_fake_arg_returns_error() {
    // Run setup.py with an unsupported argument, should return non-zero
    #[cfg(target_os = "windows")]
    let python_cmds = ["python.exe", "python3.exe"];
    #[cfg(not(target_os = "windows"))]
    let python_cmds = ["python3", "python"];

    let setup_py_path = Path::new("setup.py");
    let mut did_fail = false;

    for python in python_cmds.iter() {
        match Command::new(python)
            .arg(setup_py_path)
            .arg("--foobar123")
            .output()
        {
            Ok(output) => {
                if !output.status.success() &&
                    (!output.stdout.is_empty() || !output.stderr.is_empty())
                {
                    did_fail = true;
                    break;
                }
            }
            Err(_) => continue,
        }
    }
    assert!(did_fail, "setup.py did not fail as expected for bogus arg");
}

#[test]
fn test_setup_py_file_exists_and_has_code() {
    // setup.py should exist and contain at least some common code artifact
    let setup_py = Path::new("setup.py");
    assert!(setup_py.exists(), "setup.py not found");
    let contents = fs::read_to_string(setup_py).expect("Failed to read setup.py");
    assert!(contents.contains("setup(")
        || contents.contains("def ")
        || contents.contains("import ")
        || contents.contains("class "),
        "setup.py must contain: setup(, def, import, or class"
    );
}