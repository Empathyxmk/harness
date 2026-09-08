use scrapinghub_adblockparser::utils::split_data;

#[test]
fn test_public_split_data_titles() {
    let xs = vec!["Joe".to_string(), "amy".to_string(), "Mike".to_string(), "susan".to_string()];
    let (yes, no) = split_data(&xs, |t| t.chars().next().unwrap().is_uppercase());
    let yes: Vec<&str> = yes.into_iter().map(|s| s.as_str()).collect();
    let no: Vec<&str> = no.into_iter().map(|s| s.as_str()).collect();
    assert_eq!(yes, vec!["Joe", "Mike"]);
    assert_eq!(no, vec!["amy", "susan"]);
}

#[test]
fn test_public_split_data_all_yes() {
    let xs = vec!["Alpha".to_string(), "Beta".to_string()];
    let (yes, no) = split_data(&xs, |t| t.chars().next().unwrap().is_uppercase());
    let yes: Vec<&str> = yes.into_iter().map(|s| s.as_str()).collect();
    let no: Vec<&str> = no.into_iter().map(|s| s.as_str()).collect();
    assert_eq!(yes, vec!["Alpha", "Beta"]);
    assert_eq!(no, Vec::<&str>::new());
}

#[test]
fn test_public_split_data_all_no() {
    let xs = vec!["gamma".to_string(), "delta".to_string()];
    let (yes, no) = split_data(&xs, |t| t.chars().next().unwrap().is_uppercase());
    let yes: Vec<&str> = yes.into_iter().map(|s| s.as_str()).collect();
    let no: Vec<&str> = no.into_iter().map(|s| s.as_str()).collect();
    assert_eq!(yes, Vec::<&str>::new());
    assert_eq!(no, vec!["gamma", "delta"]);
}

#[test]
fn test_public_split_data_empty() {
    let xs: Vec<String> = vec![];
    let (yes, no) = split_data(&xs, |_t| true);
    assert_eq!(yes, Vec::<&String>::new());
    assert_eq!(no, Vec::<&String>::new());
}