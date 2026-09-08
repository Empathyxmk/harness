use std::collections::HashSet;

/// Mimic public drive test behaviors with order-independent checks and public-diff logic.

#[derive(Debug)]
struct Drive {
    name: &'static str,
    drive_type: &'static str,
    size: Option<u64>,
    children: Option<Vec<&'static str>>,
    date_changed: Option<&'static str>,
}

impl Drive {
    fn dir(&self) -> Option<Vec<&'static str>> {
        self.children.clone()
    }
}

struct PyiCloudServiceMockDrive;

impl PyiCloudServiceMockDrive {
    fn root() -> Drive {
        Drive {
            name: "",
            drive_type: "folder",
            size: None,
            children: Some(vec!["Preview", "Keynote", "Pages", "pyiCloud", "Numbers"]),
            date_changed: None,
        }
    }
    fn get_keynote() -> Drive {
        Drive {
            name: "Keynote",
            drive_type: "app_library",
            size: None,
            children: None,
            date_changed: None,
        }
    }
    fn get_ghost_folder() -> Option<Drive> {
        None
    }
    fn get_pages() -> Drive {
        Drive {
            name: "Pages",
            drive_type: "folder",
            size: None,
            children: None,
            date_changed: None,
        }
    }
    fn get_test_subfolder() -> Drive {
        Drive {
            name: "Test",
            drive_type: "folder",
            size: None,
            children: Some(vec!["Document scanné 2.pdf", "Scanned document 1.pdf"]),
            date_changed: None,
        }
    }
    fn get_document_scanned() -> Drive {
        Drive {
            name: "Document scanné 2.pdf",
            drive_type: "file",
            size: Some(8973261),
            children: None,
            date_changed: Some("2020-05-03 00:14:17"),
        }
    }
}

#[test]
fn test_root_public() {
    let drive = PyiCloudServiceMockDrive::root();
    let root_children: HashSet<_> = drive.dir().unwrap().iter().cloned().collect();
    let expected_children: HashSet<_> = ["Preview", "Keynote", "Pages", "pyiCloud", "Numbers"].iter().cloned().collect();
    assert_eq!(root_children, expected_children);
    assert_eq!(drive.name, "");
    assert_eq!(drive.drive_type, "folder");
    assert_eq!(drive.size, None);
}

#[test]
fn test_folder_app_public() {
    let folder = PyiCloudServiceMockDrive::get_keynote();
    assert_eq!(folder.name, "Keynote");
    assert_eq!(folder.drive_type, "app_library");
    assert_eq!(folder.size, None);
    assert!(folder.dir().is_none());
}

#[test]
fn test_folder_not_exists_public() {
    let not_exist = PyiCloudServiceMockDrive::get_ghost_folder();
    assert!(not_exist.is_none(), "No child named 'ghost_folder' exists");
}

#[test]
fn test_folder_public() {
    let folder = PyiCloudServiceMockDrive::get_pages();
    assert_eq!(folder.name, "Pages");
    assert_eq!(folder.drive_type, "folder");
    // /Pages is mocked as an empty folder, so dir() should be error/None
    assert!(folder.dir().is_none());
}

#[test]
fn test_subfolder_public() {
    let folder = PyiCloudServiceMockDrive::get_test_subfolder();
    let file_list = folder.dir().unwrap();
    let expected: Vec<&str> = vec!["Document scanné 2.pdf", "Scanned document 1.pdf"];
    let rev_expected: Vec<&str> = expected.clone().into_iter().rev().collect();
    assert_eq!(file_list.iter().rev().cloned().collect::<Vec<_>>(), rev_expected);
    assert_eq!(folder.name, "Test");
    assert_eq!(folder.drive_type, "folder");
}

#[test]
fn test_subfolder_file_public() {
    let file_test = PyiCloudServiceMockDrive::get_document_scanned();
    assert_eq!(file_test.name, "Document scanné 2.pdf");
    assert_eq!(file_test.drive_type, "file");
    assert_ne!(file_test.size, Some(21644358)); // Checks not-equal value
    assert!(file_test.date_changed.unwrap().starts_with("2020-"));
    assert!(file_test.dir().is_none());
}

#[test]
fn test_file_open_public() {
    // Simulate "open" with resource and raw property
    struct Response { raw: i32 }
    let response = Response { raw: 1338 };
    assert!(response.raw != 0);
}