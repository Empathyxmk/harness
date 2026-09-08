#include <gtest/gtest.h>

// Register all original test suites
// GTest will take care of running all tests in tests/original/*.cpp
int main(int argc, char **argv) {
    ::testing::InitGoogleTest(&argc, argv);
    return RUN_ALL_TESTS();
}