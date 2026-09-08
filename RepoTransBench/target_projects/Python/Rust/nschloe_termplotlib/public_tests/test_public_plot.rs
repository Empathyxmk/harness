use termplotlib::plot;

#[test]
fn test_simple_plot_different_data() {
    let y = [0, 4, 2];
    let x = [10, 15, 20];
    plot::plot(&y, &x);
}