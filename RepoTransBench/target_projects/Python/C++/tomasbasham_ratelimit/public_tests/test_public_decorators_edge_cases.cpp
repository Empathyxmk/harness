#include <gtest/gtest.h>
#include <thread>
#include <chrono>
#include "ratelimit/decorators.h"
#include "ratelimit/exception.h"

TEST(PublicDecoratorsEdgeCases, NegativePeriod) {
    ratelimit::RateLimitDecorator d(1, -2);
    int callcount = 0;
    auto f = d.wrap([&]() { callcount++; return 7; });
    EXPECT_EQ(f(), 7);
    EXPECT_THROW(f(), ratelimit::RateLimitException);
}

TEST(PublicDecoratorsEdgeCases, SleepAndRetrySucceeds) {
    ratelimit::RateLimitDecorator rl(1, 0.02);
    std::vector<double> call_times;
    auto fun = ratelimit::sleep_and_retry(rl.wrap([&](){ 
        call_times.push_back(ratelimit::system_time());
        return 17;
    }));
    EXPECT_EQ(fun(), 17);
    auto t0 = ratelimit::system_time();
    EXPECT_EQ(fun(), 17);
    EXPECT_GE(ratelimit::system_time() - t0, 0.02);
}

TEST(PublicDecoratorsEdgeCases, SleepAndRetryMultiple) {
    ratelimit::RateLimitDecorator rl(2, 0.015);
    int counter = 0;
    auto g = ratelimit::sleep_and_retry(rl.wrap([&](){ counter += 2; return counter; }));

    EXPECT_EQ(g(), 2);
    EXPECT_EQ(g(), 4);
    auto t0 = ratelimit::system_time();
    EXPECT_EQ(g(), 6);
    EXPECT_EQ(counter, 6);
    EXPECT_GE(ratelimit::system_time() - t0, 0.015);
}