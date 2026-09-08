#include <gtest/gtest.h>
#include "ratelimit/exception.h"

TEST(PublicExceptionTest, RateLimitExceptionInheritance) {
    ratelimit::RateLimitException ex("foo", 0.99);
    EXPECT_TRUE(dynamic_cast<std::exception*>(&ex) != nullptr);
    EXPECT_NO_THROW(ex.period_remaining);
}

TEST(PublicExceptionTest, ExceptionStrAndValue) {
    ratelimit::RateLimitException ex("overload", 2);
    EXPECT_STREQ(ex.what(), "overload");
    EXPECT_EQ(ex.period_remaining, 2);
}