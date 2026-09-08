#include <gtest/gtest.h>
#include <string>
#include <vector>
#include "ratelimit/init_mock.h" // Mocked C++ version of ratelimit __init__

TEST(InitModule, AllExportsExist) {
    const std::vector<std::string> all = ratelimit::mock___all__();
    for (const auto& name : all) {
        ASSERT_TRUE(ratelimit::hasattr(name)) << "Module missing export: " << name;
    }
}

TEST(InitModule, LimitsAndRateLimitedAreDecorator) {
    EXPECT_EQ(&ratelimit::limits, &ratelimit::RateLimitDecorator);
    EXPECT_EQ(&ratelimit::rate_limited, &ratelimit::RateLimitDecorator);
    EXPECT_TRUE(ratelimit::callable(ratelimit::limits));
    EXPECT_TRUE(ratelimit::callable(ratelimit::rate_limited));
}

TEST(InitModule, VersionStringExists) {
    std::string v = ratelimit::__version__;
    ASSERT_FALSE(v.empty());
    ASSERT_TRUE(v.find('.') != std::string::npos);
}