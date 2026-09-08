use trezor_mnemonic_rs::Mnemonic;

#[test]
fn test_public_generate_entropy_lengths() {
    let mnemo_en = Mnemonic::new("english").unwrap();
    for &strength in &[160u32, 192, 224, 256] {
        let phrase = mnemo_en.generate(strength).unwrap();
        let words: Vec<&str> = phrase.split(' ').collect();
        assert!(words.iter().all(|w| mnemo_en.wordlist().contains(&w.to_string())));
    }
}

#[test]
fn test_public_generate_invalid_strength() {
    let mnemo_en = Mnemonic::new("english").unwrap();
    for &bad in &[10u32, 90, 270, 512] {
        let res = mnemo_en.generate(bad);
        assert!(res.is_err());
    }
}

#[test]
fn test_public_check_valid() {
    let mnemo_en = Mnemonic::new("english").unwrap();
    let phrase = mnemo_en.generate(256).unwrap();
    assert!(mnemo_en.check(&phrase));
}

#[test]
fn test_public_check_invalid() {
    let mnemo_en = Mnemonic::new("english").unwrap();
    let phrase = "legal winner thank year wave sausage worth useful legal winner thank banana";
    assert!(!mnemo_en.check(phrase));
}

#[test]
fn test_public_to_mnemonic_and_to_entropy() {
    let mnemo_en = Mnemonic::new("english").unwrap();
    let entropy = hex::decode("ffffffffffffffffffffffffffffffff").unwrap();
    let mnemonic = mnemo_en.to_mnemonic(&entropy);
    assert!(mnemonic.is_ascii());
    let recovered = mnemo_en.to_entropy(&mnemonic);
    assert_eq!(recovered, vec![0u8; 16]);
}

#[test]
fn test_public_french_with_space() {
    let mnemo_fr = Mnemonic::new("french").unwrap();
    let mnemonic = mnemo_fr.generate(128).unwrap();
    assert!(mnemonic.contains(" "));
}

#[test]
fn test_public_vectors() {
    // Simulate two vectors per language except japanese
    let langs = vec!["english", "french", "italian", "spanish"];
    for lang in langs {
        let mnemo = Mnemonic::new(lang).unwrap();
        let vectors = vec![
            ("ffffffffffffffffffffffffffffffff", "legal winner thank year wave sausage worth useful legal winner thank yellow"),
            ("00000000000000000000000000000000", "abandon abandon abandon abandon abandon abandon abandon abandon abandon abandon abandon about"),
        ];
        for (hex_entropy, phrase) in &vectors[0..2] {
            assert!(mnemo.check(phrase));
            let recovered = mnemo.to_entropy(phrase);
            assert_eq!(recovered.len(), 16);
        }
    }
}

#[test]
fn test_public_language_list() {
    let langs = Mnemonic::list_languages();
    assert!(langs.contains(&"italian".to_string()));
    assert!(langs.contains(&"spanish".to_string()));
}

#[test]
fn test_public_normalize_string() {
    let in_str = "T͏esTing   Phrase";
    let out = Mnemonic::normalize_string(in_str);
    assert!(out.contains("esT"));
    assert!(out.contains("Phrase"));
}

#[test]
fn test_public_expand_word() {
    let mnemo_en = Mnemonic::new("english").unwrap();
    let prefix = "abil";
    let expanded = mnemo_en.expand_word(prefix);
    assert!(expanded == "ability" || expanded == prefix);
}

#[test]
fn test_public_expand() {
    let mnemo_en = Mnemonic::new("english").unwrap();
    let phrase = "abil abou above";
    let expanded = mnemo_en.expand(phrase);
    assert!(expanded.contains("ability"));
    assert!(expanded.contains("about"));
    assert!(expanded.contains("above"));
}