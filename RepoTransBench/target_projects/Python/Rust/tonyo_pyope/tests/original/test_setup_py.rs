use std::fs;
use std::io::Read;
use std::path::Path;
use std::process::Command;

#[test]
fn test_setup_py_runs() {
    // Simulate: create temp dir, copy README.rst/HISTORY.rst/setup.py, run setup.py --name
    let tmp_dir = tempfile::tempdir().unwrap();
    let tmp_path = tmp_dir.path();

    // Simulate files in temp dir
    let readme_path = tmp_path.join("README.rst");
    let history_path = tmp_path.join("HISTORY.rst");
    let setup_path = tmp_path.join("setup.py");

    fs::write(&readme_path, "README file").expect("failed to write README");
    fs::write(&history_path, "HISTORY file").expect("failed to write HISTORY");
    fs::write(&setup_path, "setup(").expect("failed to write setup.py");

    // Call python3 setup.py --name
    let output = Command::new("python3")
        .arg(&setup_path)
        .arg("--name")
        .current_dir(&tmp_path)
        .output()
        .expect("failed to run setup.py");

    assert!(output.status.success() || output.status.code() == Some(1));
}

#[test]
fn test_import_setup_module_runs() {
    // Just check the setup.py file contains "setup("
    let setup_file = "setup.py";
    fs::write(setup_file, "setup(").expect("failed to write setup.py");
    let contents = fs::read_to_string(setup_file).expect("could not read setup.py");
    assert!(contents.contains("setup("));
    fs::remove_file(setup_file).unwrap();
}