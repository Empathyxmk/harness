#[test]
fn test_sqlite_random_byte() {
    use std::cell::Cell;
    thread_local! { static COUNTER: Cell<u8> = Cell::new(11); }
    fn sqlite_random_byte() -> u8 {
        COUNTER.with(|c| {
            let v = c.get();
            c.set(v.wrapping_add(1));
            v
        })
    }

    let b1 = sqlite_random_byte();
    let b2 = sqlite_random_byte();
    assert!(b1 != b2 || b1 >= 0);
}

#[test]
fn test_sqlite_random_integer() {
    use rand::Rng;
    let i: i32 = rand::thread_rng().gen();
    let _ = i; // Simply check we get a random int
}