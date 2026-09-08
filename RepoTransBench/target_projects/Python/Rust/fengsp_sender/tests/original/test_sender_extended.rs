use fengsp_sender::Attachment;

#[test]
fn test_attachment_creation() {
    let a = Attachment::new("test.txt");
    assert_eq!(a.filename.as_deref(), Some("test.txt"));
    assert!(std::mem::size_of::<Attachment>() > 0); // instance is not None
}

#[test]
fn test_attachment_repr() {
    let a = Attachment::new("test.txt");
    let repr = format!("{:?}", a);
    assert!(repr.contains("Attachment"));
}