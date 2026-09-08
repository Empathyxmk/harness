#include <gtest/gtest.h>

// Forwards all test files in the "original" subdir.

int main(int argc, char **argv) {
    ::testing::InitGoogleTest(&argc, argv);
    return RUN_ALL_TESTS();
}