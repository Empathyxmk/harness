use protontricks::flatpak::is_flatpak;

#[test]
fn test_public_is_flatpak_env() {
    std::env::set_var("FLATPAK_ID", "foo.bar.publicprotontricks");
    assert!(is_flatpak());
}
#[test]
fn test_public_is_flatpak_env2() {
    std::env::remove_var("FLATPAK_ID");
    std::env::set_var("STEAM_FLATPAK_PRIME", "1");
    assert!(is_flatpak());
}
#[test]
fn test_public_not_flatpak() {
    std::env::remove_var("FLATPAK_ID");
    std::env::remove_var("STEAM_FLATPAK_PRIME");
    std::env::set_var("PROTONTRICKS_FLATPAK", "0");
    assert!(!is_flatpak());
}
#[test]
fn test_public_is_flatpak_env3() {
    std::env::set_var("PROTONTRICKS_FLATPAK", "1");
    std::env::remove_var("FLATPAK_ID");
    std::env::remove_var("STEAM_FLATPAK_PRIME");
    assert!(is_flatpak());
}