use termplotlib::barh;

#[test]
fn test_simple_barh_different_data() {
    let y = [6, 1, 4];
    let x = [7, 8, 9];
    barh::barh(&y, &x);
}