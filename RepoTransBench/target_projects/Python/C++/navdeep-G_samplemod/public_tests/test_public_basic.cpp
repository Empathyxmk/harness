#include <gtest/gtest.h>
#include "core.h"

TEST(PublicBasic, test_add_positive_numbers_public) {
    EXPECT_EQ(add(10, 5), 15);
}

TEST(PublicBasic, test_add_negative_and_positive_public) {
    EXPECT_EQ(add(-6, 4), -2);
}

TEST(PublicBasic, test_add_zero_public) {
    EXPECT_EQ(add(0, 19), 19);
}