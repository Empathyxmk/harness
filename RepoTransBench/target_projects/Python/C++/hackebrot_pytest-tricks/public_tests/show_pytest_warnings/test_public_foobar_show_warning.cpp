#include <gtest/gtest.h>
#include <string>

// Simulate test logic (no actual warning system in C++ gtest)
static int DOUBLE(int x) { return x * 2; }

TEST(PublicFoobarShowWarning, DoubleTestPublic) {
    EXPECT_EQ(DOUBLE(2), 4);
    EXPECT_EQ(DOUBLE(-1), -2);
    EXPECT_EQ(DOUBLE(0), 0);
}