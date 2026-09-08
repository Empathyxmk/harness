use peritus_bumpversion::bump_mod;

#[test]
fn test_known_vcs_mappings_non_git_mercurial() {
    let vcs_map = bump_mod::get_known_vcs_map();
    assert!(vcs_map.contains_key("hg"));
    assert!(vcs_map.contains_key("svn"));
}

#[test]
fn test_vcs_map_content_types() {
    let vcs_map = bump_mod::get_known_vcs_map();
    for (key, val) in vcs_map.iter() {
        assert!(!key.is_empty());
        // Just check val is a fn pointer
        let _r: bool = val();
    }
}

#[test]
fn test_default_vcs_scenarios() {
    let vcs_map = bump_mod::get_known_vcs_map();
    assert!(vcs_map.contains_key("hg") || vcs_map.contains_key("svn"));
}