#include <gtest/gtest.h>
#include "chronological.h"

TEST(TestChronologicalBranches, DummyPositive) {
    EXPECT_TRUE(dummy_positive(5));
    EXPECT_FALSE(dummy_positive(-3));
    EXPECT_FALSE(dummy_positive(0));
}