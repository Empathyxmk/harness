// Reconstructed from htmlcov/z_8884eecf70e7cb77_test_zbar_library_py.html

struct FakeCDLL {
    fail_pattern: &'static str,
}
impl FakeCDLL {
    fn load_library(&self, fname: &str) -> Result<String, &'static str> {
        if fname.contains(self.fail_pattern) {
            Err("OSError")
        } else {
            Ok(fname.to_string())
        }
    }
}

fn fake_find_library(zbar: &str) -> Option<&'static str> {
    if zbar == "zbar" {
        Some("libzbar.so")
    } else {
        None
    }
}

fn fake_find_library_none(_: &str) -> Option<&'static str> {
    None
}

#[test]
fn test_found_non_windows() {
    let cdll = FakeCDLL { fail_pattern: "fail" };
    let find_lib = fake_find_library;
    let system_name = "Not windows";
    let libname = find_lib("zbar").expect("lib found");
    let loaded = cdll.load_library(libname).expect("should load");
    assert_eq!(loaded, libname);
}

#[test]
fn test_not_found_non_windows() {
    let cdll = FakeCDLL { fail_pattern: "fail" };
    let find_lib = fake_find_library_none;
    let system_name = "Not windows";
    let lib = find_lib("zbar");
    assert!(lib.is_none());
}

#[test]
fn test_found_windows() {
    let cdll = FakeCDLL { fail_pattern: "fail" };
    let dep = cdll.load_library("dependency fname").unwrap();
    let dll = cdll.load_library("dll fname").unwrap();
    let res = (dll.clone(), vec![dep.clone()]);
    assert!(res.0.contains("dll fname"));
    assert_eq!(res.1.len(), 1);
}

#[test]
fn test_not_found_windows() {
    let cdll = FakeCDLL { fail_pattern: "fail" };
    let fail = cdll.load_library("fail dependency"); // should fail
    assert!(fail.is_err());
}

// Windows-specific _windows_fnames utility functions
fn windows_fnames(maxsize: usize) -> (&'static str, &'static [&'static str]) {
    if maxsize <= (1u64 << 32) as usize {
        ("libzbar-32.dll", &["libiconv-2.dll"])
    } else {
        ("libzbar-64.dll", &["libiconv.dll"])
    }
}

#[test]
fn test_windows_fnames_32bit() {
    let maxsize = (1u64 << 32) as usize;
    let (dll, deps) = windows_fnames(maxsize);
    assert_eq!(dll, "libzbar-32.dll");
    assert_eq!(deps, ["libiconv-2.dll"]);
}
#[test]
fn test_windows_fnames_64bit() {
    let maxsize = ((1u64 << 32) + 1) as usize;
    let (dll, deps) = windows_fnames(maxsize);
    assert_eq!(dll, "libzbar-64.dll");
    assert_eq!(deps, ["libiconv.dll"]);
}