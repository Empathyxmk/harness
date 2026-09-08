#include <gtest/gtest.h>
#include "chronological.h"

TEST(TestChronological, DummyAdd) {
    EXPECT_EQ(dummy_add(2, 3), 5);
    EXPECT_EQ(dummy_add(-1, 1), 0);
    EXPECT_EQ(dummy_add(0, 0), 0);
}