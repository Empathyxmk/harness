use termplotlib::hist;

#[test]
fn test_simple_hist() {
    let data = [1, 2, 2, 3];
    let bin_edges = [1, 2, 3];
    hist::hist(&data, &bin_edges);
}