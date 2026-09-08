#include <gtest/gtest.h>
#include <string>
#include <set>
#include "ratelimit/init_mock.h"

TEST(PublicInitModule, AllExports) {
    std::set<std::string> exported(ratelimit::mock___all__().begin(), ratelimit::mock___all__().end());
    for (const auto& name : exported) {
        ASSERT_TRUE(ratelimit::hasattr(name));
    }
}

TEST(PublicInitModule, LimitsAndRateLimitedAreDecorator) {
    EXPECT_EQ(ratelimit::repr(ratelimit::limits), ratelimit::repr(ratelimit::RateLimitDecorator));
    EXPECT_EQ(ratelimit::repr(ratelimit::rate_limited), ratelimit::repr(ratelimit::RateLimitDecorator));
    EXPECT_TRUE(ratelimit::has_call(ratelimit::limits));
    EXPECT_TRUE(ratelimit::has_call(ratelimit::rate_limited));
}

TEST(PublicInitModule, VersionStringLength) {
    std::string v = ratelimit::__version__;
    EXPECT_TRUE(typeid(v)==typeid(std::string));
    int dot_count = std::count(v.begin(), v.end(), '.');
    EXPECT_GE(dot_count, 2);
}