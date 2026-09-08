#include <gtest/gtest.h>
#include "core.h"

TEST(PublicAdvanced, test_safe_divide_normal_public) {
    EXPECT_EQ(safe_divide(15, 3), 5);
}

TEST(PublicAdvanced, test_safe_divide_negative_public) {
    EXPECT_EQ(safe_divide(-9, 3), -3);
}

TEST(PublicAdvanced, test_safe_divide_zero_dividend_public) {
    EXPECT_EQ(safe_divide(0, 2), 0);
}

TEST(PublicAdvanced, test_safe_divide_raises_zero_division_public) {
    EXPECT_THROW(safe_divide(2, 0), std::runtime_error);
}