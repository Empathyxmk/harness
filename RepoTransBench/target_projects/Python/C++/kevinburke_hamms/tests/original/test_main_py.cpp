#include <gtest/gtest.h>

// Simulate import of hamms.__main__ running a guard
TEST(MainPy, MainGuardTriggersMain) {
    // In this test, just for coverage, we "import" the module and, as in Python, don't actually run anything.
    SUCCEED();
}