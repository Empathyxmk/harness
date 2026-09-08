use termplotlib::barh;

#[test]
fn test_simple_barh() {
    let y = [3, 2, 5];
    let x = [1, 2, 3];
    barh::barh(&y, &x);
}