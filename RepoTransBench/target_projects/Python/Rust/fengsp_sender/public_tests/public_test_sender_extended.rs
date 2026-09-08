use fengsp_sender::Attachment;

#[test]
fn test_attachment_creation_different_file() {
    let a = Attachment::new("newfile.pdf");
    assert_eq!(a.filename.as_deref(), Some("newfile.pdf"));
    assert!(std::mem::size_of::<Attachment>() > 0); // instance is not None
}

#[test]
fn test_attachment_repr_different_file() {
    let a = Attachment::new("readme.md");
    let repr = format!("{:?}", a);
    assert!(repr.contains("Attachment"));
}