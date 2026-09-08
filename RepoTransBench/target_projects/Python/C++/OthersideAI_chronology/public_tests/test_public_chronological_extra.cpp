#include <gtest/gtest.h>
#include "chronological.h"

TEST(TestPublicChronologicalExtra, DummyMulPublic) {
    EXPECT_EQ(dummy_mul(4, 5), 20);
    EXPECT_EQ(dummy_mul(-2, 6), -12);
    EXPECT_EQ(dummy_mul(0, -3), 0);
}