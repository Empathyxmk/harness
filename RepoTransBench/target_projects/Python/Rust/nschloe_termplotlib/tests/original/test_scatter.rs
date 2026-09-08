use termplotlib::plot;

#[test]
fn test_simple_scatter() {
    // scatter test is implemented as a plot in Py test
    let x = [1, 2, 3];
    let y = [3, 2, 1];
    plot::plot(&y, &x);
}