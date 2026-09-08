use scrapinghub_adblockparser::utils::split_data;

#[test]
fn test_split_data_titles() {
    let xs = vec!["foo".to_string(), "Bar".to_string(), "Spam".to_string(), "egg".to_string()];
    let (yes, no): (Vec<&String>, Vec<&String>) = split_data(&xs, |t| t.chars().next().unwrap().is_uppercase());
    let yes: Vec<&str> = yes.into_iter().map(|s| s.as_str()).collect();
    let no: Vec<&str> = no.into_iter().map(|s| s.as_str()).collect();
    assert_eq!(yes, vec!["Bar", "Spam"]);
    assert_eq!(no, vec!["foo", "egg"]);
}

#[test]
fn test_split_data_all_yes() {
    let xs = vec!["Hello".to_string(), "World".to_string()];
    let (yes, no) = split_data(&xs, |t| t.chars().next().unwrap().is_uppercase());
    let yes: Vec<&str> = yes.into_iter().map(|s| s.as_str()).collect();
    let no: Vec<&str> = no.into_iter().map(|s| s.as_str()).collect();
    assert_eq!(yes, vec!["Hello", "World"]);
    assert_eq!(no, Vec::<&str>::new());
}

#[test]
fn test_split_data_all_no() {
    let xs = vec!["foo".to_string(), "bar".to_string()];
    let (yes, no) = split_data(&xs, |t| t.chars().next().unwrap().is_uppercase());
    let yes: Vec<&str> = yes.into_iter().map(|s| s.as_str()).collect();
    let no: Vec<&str> = no.into_iter().map(|s| s.as_str()).collect();
    assert_eq!(yes, Vec::<&str>::new());
    assert_eq!(no, vec!["foo", "bar"]);
}

#[test]
fn test_split_data_empty() {
    let xs: Vec<String> = vec![];
    let (yes, no) = split_data(&xs, |_t| false);
    assert_eq!(yes, Vec::<&String>::new());
    assert_eq!(no, Vec::<&String>::new());
}