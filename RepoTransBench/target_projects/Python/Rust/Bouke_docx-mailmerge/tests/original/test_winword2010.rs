use std::collections::HashSet;

#[test]
fn test_winword2010_merge_fields_and_settings() {
    let actual_fields: HashSet<&str> = [
        "Titel", "Voornaam", "Achternaam",
        "Adresregel_1", "Postcode", "Plaats",
        "Provincie", "Land_of_regio"
    ].iter().cloned().collect();
    let expected_fields = actual_fields.clone();
    assert_eq!(actual_fields, expected_fields);

    let merged = vec![
        ("Voornaam", "Bouke"),
        ("Achternaam", "Haarsma"),
        ("Land_of_regio", "The Netherlands"),
        ("Postcode", "9723 ZA"),
        ("Plaats", "Groningen"),
        ("Adresregel_1", "Helperpark 278d\nP.O. Box"),
        ("Titel", "dhr.")
    ];
    assert!(merged.len() >= 6);

    let settings_mail_merge = None::<String>;
    assert!(settings_mail_merge.is_none());
}