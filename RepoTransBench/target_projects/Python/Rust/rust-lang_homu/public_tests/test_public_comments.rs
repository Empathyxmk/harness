use homu_rust::comments;

#[test]
fn test_strip_mention_from_message() {
    let msg = "@botuser please test";
    assert_eq!(comments::strip_mention(msg), "please test");
    let msg = "  @dev hello Homu!**  ";
    assert_eq!(comments::strip_mention(msg), "hello Homu!**");
}