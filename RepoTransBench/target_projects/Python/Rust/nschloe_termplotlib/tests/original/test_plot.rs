use termplotlib::plot::plot;

#[test]
fn test_simple_plot() {
    let y = [2, 3, 1];
    let x = [1, 2, 3];
    plot(&y, &x);
}