#include <gtest/gtest.h>
#include "ratelimit/exception.h"

TEST(RateLimitExceptionTests, Fields) {
    ratelimit::RateLimitException e("too many", 3.5);
    EXPECT_EQ(std::string(e.what()), "too many");
    EXPECT_DOUBLE_EQ(e.period_remaining, 3.5);
}