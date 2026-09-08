use termplotlib::figure::{Figure, Axes};

#[test]
fn test_figure_creation_and_axes() {
    let mut f = Figure::new();
    // Add an axis and ensure it's an Axes object
    let ax = f.add_subplot(111);
    // Assert its type is Axes
    let _t: &Axes = &ax;
    // Add a second axis and test it's also an Axes object
    let ax2 = f.add_subplot(112);
    let _t2: &Axes = &ax2;
    // Check different axes are not the same
    assert_ne!(ax.id, ax2.id, "Axes created should be different objects");
}