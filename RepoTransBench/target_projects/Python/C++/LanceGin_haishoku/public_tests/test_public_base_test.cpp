#include <gtest/gtest.h>

TEST(TestPublicBase, true_is_true_public) {
    EXPECT_TRUE(true);
}

TEST(TestPublicBase, arithmetic_public) {
    EXPECT_EQ(7-3, 4);
}