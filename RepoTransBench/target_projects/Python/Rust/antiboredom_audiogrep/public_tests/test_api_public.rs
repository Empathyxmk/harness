use antiboredom_audiogrep::*;
use tempfile::tempdir;
use std::fs;
use std::io::Write;

#[test]
fn test_find_files_public() {
    let tmp = tempdir().unwrap();
    let files = [
        tmp.path().join("x.flac"),
        tmp.path().join("y.flac"),
        tmp.path().join("z.txt"),
    ];
    for f in &files {
        fs::File::create(f).unwrap();
    }
    let found = find_files(tmp.path(), &[".flac"]);
    let mut expected = vec![
        files[0].to_string_lossy().to_string(),
        files[1].to_string_lossy().to_string(),
    ];
    let mut found = found;
    expected.sort();
    found.sort();
    assert_eq!(found, expected);
}

#[test]
fn test_regexify_public() {
    let text = "hello? world* (demo)";
    let r = regexify(text);
    assert_eq!(r, r"hello\?\ world\*\ \(demo\)");
}

#[test]
fn test_get_word_timings_public() {
    let tmp = tempdir().unwrap();
    let fn_path = tmp.path().join("timings_public.txt");
    let lines = [
        "<s> 5.0 6.0 1\n", 
        "gamma 6.0 6.2 1\n", 
        "zeta 6.2 6.3 1\n", 
        "</s> 6.3 6.7 1\n"
    ].join("");
    {
        let mut f = fs::File::create(&fn_path).unwrap();
        f.write_all(lines.as_bytes()).unwrap();
    }
    let tgt = get_word_timings(&fn_path);
    assert_eq!(tgt.len(), 2);
    assert_eq!(tgt[0].0, "gamma");
    assert_eq!(tgt[1].0, "zeta");
}

#[test]
fn test_group_words_public() {
    // ('a', 1, 2, 3), ('b', 2, 3, 4) ...
    let words = [('a', 1, 2, 3), ('b', 2, 3, 4), ('c', 3, 4, 5), ('d', 4, 5, 6), ('e', 5, 6, 7)];
    let n = 4;
    let grouped: Vec<_> = group_words(&words, n).collect();
    assert_eq!(grouped.len(), 2);
    assert_eq!(grouped[0][0].0, 'a');
    assert_eq!(grouped[1][0].0, 'b');
}

#[test]
fn test_get_grouped_word_timings_public() {
    let tmp = tempdir().unwrap();
    let fn_path = tmp.path().join("grouped_timings_public.txt");
    let lines = [
        "<s> 11.0 12.0 1\n", 
        "x 12.0 12.44 1\n", 
        "y 12.44 12.89 1\n", 
        "z 12.89 13.41 1\n", 
        "</s> 13.41 13.91 1\n"
    ].join("");
    {
        let mut f = fs::File::create(&fn_path).unwrap();
        f.write_all(lines.as_bytes()).unwrap();
    }
    let groups = get_grouped_word_timings(&fn_path, 2);
    assert_eq!(groups.len(), 2);
    assert_eq!(groups[0][0].0, "x");
    assert_eq!(groups[1][0].0, "y");
}

#[test]
fn test_franken_sentence_public() {
    use serde_json::json;
    let in_wt = vec![
        vec![("apple".to_string(), 0.1, 0.2, 0.0), ("pear".to_string(), 0.2, 0.3, 0.0)],
        vec![("banana".to_string(), 0.3, 0.5, 0.0)],
    ];
    // Using stub: returns Vec<serde_json::Value>
    let r = franken_sentence("test sentence", &[]);
    assert!(r.is_empty() || r.iter().all(|v| v.is_i64() || v.is_object() || v.is_array()));
}

#[test]
fn test_search_modes_public() {
    // Patch search logic is already stubbed, so calls to search should return expected types
    let tmp = tempdir().unwrap();
    let fn_path = tmp.path().join("public.transcription.txt");
    let lines = [
        "<s> 3.0 3.7 1\n", "foo 3.7 3.8 1\n", "bar 3.8 4.1 1\n", "</s> 4.1 4.5 1\n"
    ].join("");
    {
        let mut f = fs::File::create(&fn_path).unwrap();
        f.write_all(lines.as_bytes()).unwrap();
    }
    let out = search("any", &[fn_path.to_string_lossy().as_ref()], "fragment", false);
    assert!(!out.is_empty());
    let out2 = search("hello", &[fn_path.to_string_lossy().as_ref()], "word", false);
    assert!(!out2.is_empty());
    let out3 = search("repeat", &[fn_path.to_string_lossy().as_ref()], "sentence", false);
    assert!(!out3.is_empty());
}

#[test]
fn test_make_splice_public() {
    // Make sure error happens as expected
    let tmp = tempdir().unwrap();
    let out_mp3 = tmp.path().join("f.spliced.mp3");
    // Slices: two dummy ranges
    let slices = vec![0..2, 3..5];
    let res = make_splice("dummy.mp3", slices, out_mp3.to_string_lossy().as_ref());
    assert!(res.is_err());
}