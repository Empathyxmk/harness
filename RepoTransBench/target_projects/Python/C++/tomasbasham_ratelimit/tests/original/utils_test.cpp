#include <gtest/gtest.h>
#include <thread>
#include <chrono>
#include "ratelimit/utils.h"

TEST(Utils, NowReturnsCallableAndFloat) {
    auto monotonic_or_time = ratelimit::now();
    double v = monotonic_or_time();
    EXPECT_TRUE(typeid(v)==typeid(double));
}

TEST(Utils, NowFallback) {
    // Simulate fallback by calling with force_time = true
    auto fn = ratelimit::now(/*force_time*/true);
    EXPECT_TRUE(typeid(fn())==typeid(double));
    EXPECT_NEAR(fn(), ratelimit::system_time(), 1.0);
}