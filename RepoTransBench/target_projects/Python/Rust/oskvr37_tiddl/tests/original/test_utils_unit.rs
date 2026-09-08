#[cfg(test)]
mod tests {
    use std::fs;
    use std::path::Path;
    use tempfile::tempdir;
    use crate::utils::*;

    #[test]
    fn test_safe_filename_with_badchars() {
        let s = "hello/\\:*?\"<>|world";
        let out = safe_filename(s);
        assert!(!out.contains('/'));
        assert!(!out.contains('\\'));
        assert!(!out.contains(':'));
        assert!(!out.contains('?'));
        assert!(!out.contains('<'));
        assert!(!out.contains('>'));
        assert!(!out.contains('|'));
    }

    #[test]
    fn test_make_dir_and_file() {
        let dir = tempdir().unwrap();
        let d = dir.path().join("a/b");
        makedir(&d);
        assert!(d.exists() && d.is_dir());
        let file = dir.path().join("file.txt");
        fs::File::create(&file).unwrap();
        let new_file = dir.path().join("copy.txt");
        copy_file(&file, &new_file);
        assert!(new_file.exists());
    }

    #[test]
    fn test_delete_and_exists() {
        let dir = tempdir().unwrap();
        let f = dir.path().join("f.txt");
        {
            let mut fh = fs::File::create(&f).unwrap();
            write!(fh, "abc").unwrap();
        }
        assert!(file_exists(&f));
        remove_file(&f);
        assert!(!file_exists(&f));
        let d = dir.path().join("some-dir");
        makedir(&d);
        remove_dir(&d);
        assert!(!d.exists());
    }

    #[test]
    fn test_stringify_simple() {
        let obj = serde_json::json!({"a": 1});
        let out = stringify(&obj);
        assert!(out.starts_with('{'));
    }

    #[test]
    fn test_humanize_size() {
        assert_eq!(humanize_size(512), "512 B");
        let mb = humanize_size(1024 * 1024);
        assert!(mb.contains("MB"));
    }

    #[test]
    fn test_format_seconds() {
        assert_eq!(format_seconds(65), "1:05");
        assert_eq!(format_seconds(3661), "1:01:01");
    }

    #[test]
    fn test_calc_segments_chunks() {
        let items = (0..10).collect::<Vec<_>>();
        let chunks_list = chunks(items.clone(), 3);
        for chunk in &chunks_list {
            assert!(chunk.is_vec());
        }
        // segments
        let urls = vec!["a", "b"];
        let out = calc_segments(urls, 10.0);
        assert!(out.is_vec());
    }

    #[test]
    fn test_path_to_uri() {
        let f = Path::new("/file.txt");
        let uri = path_to_uri(f);
        assert!(uri.starts_with("file:"));
    }

    #[test]
    fn test_try_int_ok_and_fail() {
        assert_eq!(try_int("123", None), 123);
        assert_eq!(try_int("fail", Some(-1)), -1);
    }

    #[test]
    fn test_flatten_and_take() {
        let data = vec![vec![1, 2], vec![3, 4]];
        let out = flatten(data);
        assert_eq!(out, vec![1, 2, 3, 4]);
        let out2 = take(0..5, 3);
        assert_eq!(out2, vec![0, 1, 2]);
    }

    #[test]
    fn test_files_and_dirs() {
        let dir = tempdir().unwrap();
        // For this simplified port, test that directories and files can be listed
        let d = dir.path().join("d");
        makedir(&d);
        let f = d.join("f.txt");
        std::fs::write(&f, "ok").unwrap();
        let files: Vec<_> =
            fs::read_dir(&d).unwrap().filter_map(Result::ok).filter(|e| e.path().is_file()).collect();
        let dirs: Vec<_> =
            fs::read_dir(dir.path()).unwrap().filter_map(Result::ok).filter(|e| e.path().is_dir()).collect();
        assert!(!files.is_empty());
        assert!(!dirs.is_empty());
    }
}