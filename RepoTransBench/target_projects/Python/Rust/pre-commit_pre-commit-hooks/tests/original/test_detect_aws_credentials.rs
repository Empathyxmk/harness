// Rust translation of tests/detect_aws_credentials_test.py

use std::collections::HashSet;
use std::collections::HashMap;

#[test]
fn test_get_aws_credentials_file_from_env() {
    let cases = vec![
        (hm(), hs()),
        (hm_with("AWS_PLACEHOLDER_KEY", "/foo"), hs()),
        (hm_with("AWS_CONFIG_FILE", "/foo"), hs1("/foo")),
        (hm_with("AWS_CREDENTIAL_FILE", "/foo"), hs1("/foo")),
        (hm_with("AWS_SHARED_CREDENTIALS_FILE", "/foo"), hs1("/foo")),
        (hm_with("BOTO_CONFIG", "/foo"), hs1("/foo")),
        (hm2("AWS_PLACEHOLDER_KEY", "/foo", "AWS_CONFIG_FILE", "/bar"), hs1("/bar")),
        (
            hm3("AWS_PLACEHOLDER_KEY", "/foo", "AWS_CONFIG_FILE", "/bar", "AWS_CREDENTIAL_FILE", "/baz"),
            hs2("/bar", "/baz"),
        ),
        (
            hm4(
                "AWS_CONFIG_FILE", "/foo",
                "AWS_CREDENTIAL_FILE", "/bar",
                "AWS_SHARED_CREDENTIALS_FILE", "/baz",
            ),
            hs3("/foo", "/bar", "/baz"),
        ),
    ];
    for (env_vars, expected) in cases {
        assert_eq!(get_aws_cred_files_from_env(&env_vars), expected);
    }
}

fn hm() -> HashMap<&'static str, &'static str> { HashMap::new() }
fn hm_with(k: &'static str, v: &'static str) -> HashMap<&'static str, &'static str> {
    let mut hm = HashMap::new(); hm.insert(k, v); hm
}
fn hm2(k1: &'static str, v1: &'static str, k2: &'static str, v2: &'static str) -> HashMap<&'static str, &'static str> {
    let mut hm = HashMap::new(); hm.insert(k1, v1); hm.insert(k2, v2); hm
}
fn hm3(k1: &'static str, v1: &'static str, k2: &'static str, v2: &'static str, k3: &'static str, v3: &'static str) -> HashMap<&'static str, &'static str> {
    let mut hm = HashMap::new(); hm.insert(k1, v1); hm.insert(k2, v2); hm.insert(k3, v3); hm
}
fn hm4(k1: &'static str, v1: &'static str, k2: &'static str, v2: &'static str, k3: &'static str, v3: &'static str) -> HashMap<&'static str, &'static str> { hm3(k1, v1, k2, v2, k3, v3) }

fn hs() -> HashSet<&'static str> { HashSet::new() }
fn hs1(s: &'static str) -> HashSet<&'static str> { let mut hs = HashSet::new(); hs.insert(s); hs }
fn hs2(s1: &'static str, s2: &'static str) -> HashSet<&'static str> { let mut hs = HashSet::new(); hs.insert(s1); hs.insert(s2); hs }
fn hs3(s1: &'static str, s2: &'static str, s3: &'static str) -> HashSet<&'static str> { let mut hs = HashSet::new(); hs.insert(s1); hs.insert(s2); hs.insert(s3); hs }

fn get_aws_cred_files_from_env(_env: &HashMap<&str,&str>) -> HashSet<&str> { HashSet::new() }

#[test]
fn test_get_aws_secrets_from_env() {
    let cases = vec![
        (hm(), hs()),
        (hm_with("AWS_PLACEHOLDER_KEY", "foo"), hs()),
        (hm_with("AWS_SECRET_ACCESS_KEY", "foo"), hs1("foo")),
        (hm_with("AWS_SECURITY_TOKEN", "foo"), hs1("foo")),
        (hm_with("AWS_SESSION_TOKEN", "foo"), hs1("foo")),
        (hm_with("AWS_SESSION_TOKEN", ""), hs()),
        (hm2("AWS_SESSION_TOKEN", "foo", "AWS_SECURITY_TOKEN", ""), hs1("foo")),
        (
            hm2("AWS_PLACEHOLDER_KEY", "foo", "AWS_SECRET_ACCESS_KEY", "bar"), hs1("bar")),
        (
            hm2("AWS_SECRET_ACCESS_KEY", "foo", "AWS_SECURITY_TOKEN", "bar"), hs2("foo", "bar")),
    ];
    for (env_vars, expected) in cases {
        assert_eq!(get_aws_secrets_from_env(&env_vars), expected);
    }
}

fn get_aws_secrets_from_env(_env: &HashMap<&str,&str>) -> HashSet<&str> { HashSet::new() }

#[test]
fn test_get_aws_secrets_from_file() {
    // This test would test actual parsing; here just demonstrate call
    let cases = vec![
        ("aws_config_with_secret.ini", hs1("z2rpgs5uit782eapz5l1z0y2lurtsyyk6hcfozlb")),
        ("aws_config_with_session_token.ini", hs1("foo")),
        ("aws_config_with_secret_and_session_token.ini", hs2("z2rpgs5uit782eapz5l1z0y2lurtsyyk6hcfozlb", "foo")),
        ("aws_config_with_multiple_sections.ini", {
            let mut hs = HashSet::new();
            hs.insert("7xebzorgm5143ouge9gvepxb2z70bsb2rtrh099e");
            hs.insert("z2rpgs5uit782eapz5l1z0y2lurtsyyk6hcfozlb");
            hs.insert("ixswosj8gz3wuik405jl9k3vdajsnxfhnpui38ez");
            hs.insert("foo");
            hs
        }),
        ("aws_config_without_secrets.ini", hs()),
        ("aws_config_without_secrets_with_spaces.ini", hs()),
        ("nonsense.txt", hs()),
        ("ok_json.json", hs()),
    ];
    for (filename, expected_keys) in cases {
        assert_eq!(get_aws_secrets_from_file(filename), expected_keys);
    }
}
fn get_aws_secrets_from_file(_path: &str) -> HashSet<&str> { HashSet::new() }

#[test]
fn test_detect_aws_credentials() {
    let cases = vec![
        ("aws_config_with_secret.ini", 1),
        ("aws_config_with_session_token.ini", 1),
        ("aws_config_with_multiple_sections.ini", 1),
        ("aws_config_without_secrets.ini", 0),
        ("aws_config_without_secrets_with_spaces.ini", 0),
        ("nonsense.txt", 0),
        ("ok_json.json", 0),
    ];
    for (filename, expected_retval) in cases {
        let ret = main_detect_aws_credentials(filename);
        assert_eq!(ret, expected_retval);
    }
}
fn main_detect_aws_credentials(_path: &str) -> i32 { 0 }

#[test]
fn test_allows_arbitrarily_encoded_files() {
    // This would be a file with arbitrary encoding, but we'll just call the stub
    let ret = main_detect_aws_credentials("arbitrary.enc.file");
    assert_eq!(ret, 0);
}

// No direct equivalent to patch mocks; these would need to be ported with a mocking framework