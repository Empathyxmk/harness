#include "gtest/gtest.h"

// Register all tests from tests/ and public_tests/
// (All tests will be visible once test_runner executable is linked with all *_test.cpp files)

int main(int argc, char **argv) {
    ::testing::InitGoogleTest(&argc, argv);
    return RUN_ALL_TESTS();
}