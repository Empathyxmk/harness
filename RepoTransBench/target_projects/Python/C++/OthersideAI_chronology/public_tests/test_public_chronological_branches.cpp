#include <gtest/gtest.h>
#include "chronological.h"

TEST(TestPublicChronologicalBranches, DummyPositivePublic) {
    EXPECT_TRUE(dummy_positive(42));
    EXPECT_FALSE(dummy_positive(-17));
    EXPECT_FALSE(dummy_positive(0));
}