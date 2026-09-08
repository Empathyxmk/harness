#include <gtest/gtest.h>
#include "ratelimit/exception.h"

TEST(RateLimitExceptionTests, MessageAndPeriod) {
    ratelimit::RateLimitException e("limit reached", 4.5);
    EXPECT_DOUBLE_EQ(e.period_remaining, 4.5);
    EXPECT_STREQ(e.what(), "limit reached");
}