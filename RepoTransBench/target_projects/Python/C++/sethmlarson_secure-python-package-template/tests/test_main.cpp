#include <gtest/gtest.h>

// This file is just needed to provide a test main for GoogleTest
int main(int argc, char** argv) {
    ::testing::InitGoogleTest(&argc, argv);
    return RUN_ALL_TESTS();
}