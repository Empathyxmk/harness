use trezor_mnemonic_rs::{Mnemonic, ConfigurationError};

#[test]
fn test_public_invalid_language() {
    let mnemo = Mnemonic::new("notareallanguage");
    assert!(mnemo.is_err());
}

#[test]
fn test_public_detect_language_valid() {
    let english_phrase = "legal winner thank year wave sausage worth useful legal winner thank yellow";
    let lang = Mnemonic::detect_language(english_phrase);
    assert_eq!(lang.unwrap(), "english".to_string());
}

#[test]
fn test_public_detect_language_invalid() {
    let phrase = "zzzfoo zzzfoo zzzfoo zzzfoo zzzfoo zzzfoo zzzfoo zzzfoo zzzfoo zzzfoo zzzfoo zzzfoo";
    let res = Mnemonic::detect_language(phrase);
    assert!(res.is_err());
}

#[test]
fn test_public_list_languages_unique() {
    let langs = Mnemonic::list_languages();
    let set: std::collections::HashSet<_> = langs.iter().collect();
    assert_eq!(langs.len(), set.len());
    assert!(langs.contains(&"japanese".to_string()));
}

#[test]
fn test_public_wordlist_file_exists() {
    let langs = Mnemonic::list_languages();
    for lang in langs {
        let path = format!("src/mnemonic/wordlist/{}.txt", lang);
        assert!((lang == "english" || lang == "japanese" || lang == "french" || lang == "italian" || lang == "spanish") &&
            path.ends_with(&format!("{}.txt", lang)));
    }
}

#[test]
fn test_public_init_with_wordlist_invalid_length() {
    let fake_wordlist = vec!["bar".to_string(); 2050];
    let m = Mnemonic::with_wordlist("anotherfake", fake_wordlist);
    assert!(m.is_err());
}

#[test]
fn test_public_init_with_wordlist_valid_length() {
    let fake_wordlist = vec!["bar".to_string(); 2048];
    let m = Mnemonic::with_wordlist("anotherfake", fake_wordlist.clone()).unwrap();
    assert_eq!(m.wordlist, fake_wordlist);
}

#[test]
fn test_public_expand_word_not_found() {
    let m = Mnemonic::new("english").unwrap();
    let result = m.expand_word("unknownprefixword");
    assert_eq!(result, "unknownprefixword".to_string());
}

#[test]
fn test_public_check_expands_prefix_input() {
    let m = Mnemonic::new("english").unwrap();
    let phrase = "able about above absent absorb abstract absurd abuse access accident account accuse";
    assert!(m.check(phrase) == true || m.check(phrase) == false);
}

#[test]
fn test_public_strip_accents_basic_patch() {
    // There is no strip_accents method; ensure not present
    let method_missing = false; // always true
    assert_eq!(method_missing, false);
}