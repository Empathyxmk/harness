// Rust test "suite" matching C++ Tester.cpp runner for aspone_OrderBook

#[cfg(test)]
mod test_suite {
    use super::*;
    // Individual test modules must be included through mod statements
    // (these will load the actual test functions)

    #[test]
    fn run_suite() {
        // This will simply run, relying on Rust's test harness to run all real tests
        println!("Testing DLList...");
        crate::tests::original::test_dllist::test_dllist_basic();
        
        println!("Testing CountedOrderList...");
        crate::tests::original::test_counted_order_list::test_counted_order_list_basic();
        crate::tests::original::test_counted_order_list::test_counted_order_list_clear_level();

        println!("Testing LagHistogram...");
        crate::tests::original::test_laghistogram::test_laghistogram_basic();
        crate::tests::original::test_laghistogram::test_laghistogram_percentiles();

        println!("Testing Logger...");
        crate::tests::original::test_logger::test_logger_basic();
        crate::tests::original::test_logger::test_logger_destructor_on_unused();
        crate::tests::original::test_logger::test_logger_multiple();

        println!("Testing HRTimer...");
        crate::tests::original::test_hrtimer::test_hrtimer_basic();
        crate::tests::original::test_hrtimer::test_hrtimer_double_stop();
        crate::tests::original::test_hrtimer::test_hrtimer_no_start();

        println!("All tests passed!");
    }
}