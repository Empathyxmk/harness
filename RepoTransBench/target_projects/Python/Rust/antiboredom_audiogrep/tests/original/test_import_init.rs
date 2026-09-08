#[test]
fn test_import_from_init() {
    // In Rust, just confirm the existence of the expected functions
    // These are module-level functions so we just call them to confirm linking
    use antiboredom_audiogrep::{convert_to_wav, transcribe};
    let _ = convert_to_wav as fn(&[&str]) -> Vec<String>;
    let _ = transcribe as fn(&[&str], usize, usize) -> ();
}