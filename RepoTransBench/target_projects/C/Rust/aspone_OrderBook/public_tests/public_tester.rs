// Translated from PublicTester.cpp: Public test runner for aspone_OrderBook

#[test]
fn run_public_logger_tests() {
    // Uses test harness to run the individual logger tests
    super::public_test_logger::public_test_logger_basic();
    super::public_test_logger::public_test_logger_destructor_on_unused();
    super::public_test_logger::public_test_logger_multiple();
}

#[test]
fn run_public_hrtimer_tests() {
    super::public_test_hrtimer::public_test_hrtimer_basic();
    super::public_test_hrtimer::public_test_hrtimer_double_stop();
    super::public_test_hrtimer::public_test_hrtimer_no_start();
}

// All public tests will be detected automatically by Rust's test harness.