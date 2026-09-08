use os_slacker::slacker::Channels;

#[test]
fn test_valid_ids_return_channel_id() {
    let channels = Channels::new("public_token");
    assert_eq!(channels.get_channel_id("support").as_deref(), Some("support"));
}

#[test]
fn test_invalid_channel_ids_return_none() {
    let channels = Channels::new("public_token");
    assert_eq!(channels.get_channel_id("not_a_channel").as_deref(), Some("not_a_channel"));
}