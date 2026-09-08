use termplotlib::subplot::Subplot;

#[test]
fn test_subplot_init() {
    // In the Python test, any class in subplot_mod is used; here we directly use Subplot
    let sp = Subplot::new((3, 3), 7);
    // Type assertion: ensure it's a Subplot (rust typing suffices)
    let _t: &Subplot = &sp;
}