use termplotlib::plot;

#[test]
fn test_simple_scatter_different_data() {
    let x = [4, 5, 6];
    let y = [6, 5, 4];
    plot::plot(&y, &x);
}