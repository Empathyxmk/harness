use termplotlib::figure::Figure;

#[test]
fn test_figure_init() {
    let fig = Figure::new();
    // Assert type
    let _t: &Figure = &fig;
}