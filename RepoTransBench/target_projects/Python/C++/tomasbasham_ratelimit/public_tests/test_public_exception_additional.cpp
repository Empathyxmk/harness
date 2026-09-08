#include <gtest/gtest.h>
#include "ratelimit/exception.h"

TEST(PublicExceptionAdditional, RateLimitExceptionFields) {
    ratelimit::RateLimitException e("limit reached", 1.25);
    EXPECT_STREQ(e.what(), "limit reached");
    EXPECT_NEAR(e.period_remaining, 1.25, 1e-9);
}