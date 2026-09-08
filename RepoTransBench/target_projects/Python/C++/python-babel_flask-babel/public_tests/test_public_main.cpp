#include <gtest/gtest.h>

// Register all public test suites; all test_public_*.cpp should be built into this target.
int main(int argc, char **argv) {
    ::testing::InitGoogleTest(&argc, argv);
    return RUN_ALL_TESTS();
}