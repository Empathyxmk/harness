use termplotlib::hist;

#[test]
fn test_simple_hist_diff_data() {
    // Only pass data, do NOT use keyword 'bins'
    let data = [3, 6, 9, 3, 6, 9, 9];
    hist::hist_bins(&data, 3);
}

#[test]
fn test_hist_label_and_ascii() {
    let data = [7, 1, 6, 8, 7, 5, 5];
    hist::hist_advanced(
        &data, 2,
        "New Title", "Alternate X", "Alternate Y", true, true
    );
}