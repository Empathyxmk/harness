#[test]
fn test_fork() {
    // Simulate forking different serializers (in Python: fork instances with different behavior).
    fn f1_serializer(_s: &str) -> &'static str { "f1" }
    fn f2_serializer(_s: &str) -> &'static str { "f2" }
    fn f3_serializer_int(_i: &i32) -> i32 { 3 }
    fn f3_serializer_str(_s: &str) -> &'static str { "f3" }
    // Simulate "forks"
    let using_f1 = f1_serializer("I wanted a fork on the table.");
    let using_f2 = f2_serializer("I wanted a fork on the table.");
    let using_f3str = f3_serializer_str("f3");
    let using_f3int = f3_serializer_int(&42);
    let using_f4 = f1_serializer("I wanted a fork on the table."); // f4 is forked from f1

    assert_eq!("f1", using_f1);
    assert_eq!("f2", using_f2);
    assert_eq!("f3", using_f3str);
    assert_eq!(3, using_f3int);
    assert_eq!("f1", using_f4);
}