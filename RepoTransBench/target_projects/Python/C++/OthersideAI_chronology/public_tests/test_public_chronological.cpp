#include <gtest/gtest.h>
#include "chronological.h"

TEST(TestPublicChronological, DummyAddPublic) {
    EXPECT_EQ(dummy_add(8, 4), 12);
    EXPECT_EQ(dummy_add(-5, 10), 5);
    EXPECT_EQ(dummy_add(7, -7), 0);
}