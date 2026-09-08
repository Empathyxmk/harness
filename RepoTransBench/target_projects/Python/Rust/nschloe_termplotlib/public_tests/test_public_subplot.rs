use termplotlib::subplot::Subplot;

#[test]
fn test_subplot_init_different_data() {
    // In Py test, finds any class. Here, use Subplot directly.
    let sp = Subplot::new((2, 4), 5);
    let _t: &Subplot = &sp;
}