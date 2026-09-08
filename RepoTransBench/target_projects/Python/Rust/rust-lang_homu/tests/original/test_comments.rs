use homu_rust::comments;

#[test]
fn test_strip_mention() {
    let msg = "@homu r+";
    assert_eq!(comments::strip_mention(msg), "r+");
    let msg = " @Homu  approve please! ";
    assert_eq!(comments::strip_mention(msg), "approve please!");
}