use crate::export::upstart::*;

#[test]
fn test_get_job_name_public() {
    assert_eq!(get_job_name("myapp", "task", 4), "myapp-task-4");
    assert_eq!(get_job_name("zebra", "stripe", 7), "zebra-stripe-7");
}
#[test]
fn test_get_master_name_public() {
    assert_eq!(get_master_name("newapp"), "newapp-master");
    assert_eq!(get_master_name("rocket"), "rocket-master");
}