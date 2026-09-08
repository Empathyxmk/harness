use seatgeek_fuzzywuzzy::process;

#[test]
fn test_extract_one_public() {
    let query = "python programmer";
    let choices = vec!["java developer", "python engineer", "c++ guru"];
    let res = process::extract_one(query, choices.iter().map(|x| *x));
    assert!(res.is_some());
    let (m, score) = res.unwrap();
    assert!(choices.contains(&m));
    assert!(score > 0);
}

#[test]
fn test_extract_bests_public() {
    let query = "data science";
    let choices = vec!["science data", "data analytics", "data scientist", "big data"];
    let res = process::extract_bests(query, &choices, None, None, None, Some(2));
    assert_eq!(res.len(), 2);
    for (m, score) in res.iter() {
        assert!(choices.contains(m));
        assert!(*score > 0);
    }
}