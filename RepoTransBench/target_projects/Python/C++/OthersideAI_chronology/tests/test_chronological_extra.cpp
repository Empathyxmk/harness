#include <gtest/gtest.h>
#include "chronological.h"

TEST(TestChronologicalExtra, DummyMul) {
    EXPECT_EQ(dummy_mul(2, 3), 6);
    EXPECT_EQ(dummy_mul(-1, 1), -1);
    EXPECT_EQ(dummy_mul(0, 5), 0);
}