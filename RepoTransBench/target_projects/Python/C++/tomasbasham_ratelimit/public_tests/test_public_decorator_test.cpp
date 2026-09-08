#include <gtest/gtest.h>
#include <thread>
#include <chrono>
#include "ratelimit/decorators.h"
#include "ratelimit/exception.h"

TEST(PublicDecoratorTest, SimpleLimit) {
    ratelimit::RateLimitDecorator d(3, 0.04);
    std::vector<int> calls;
    auto myfun = d.wrap([&calls](){ calls.push_back(2); return std::accumulate(calls.begin(), calls.end(), 0); });
    EXPECT_EQ(myfun(), 2);
    EXPECT_EQ(myfun(), 4);
    EXPECT_EQ(myfun(), 6);
    EXPECT_THROW(myfun(), ratelimit::RateLimitException);
    std::this_thread::sleep_for(std::chrono::milliseconds(45));
    EXPECT_EQ(myfun(), 8);
}

TEST(PublicDecoratorTest, SleepAndRetry) {
    ratelimit::RateLimitDecorator d(1, 0.02);
    auto fn = ratelimit::sleep_and_retry(d.wrap([](){ return 24; }));
    EXPECT_EQ(fn(), 24);
    auto t0 = ratelimit::system_time();
    EXPECT_EQ(fn(), 24);
    EXPECT_GE(ratelimit::system_time() - t0, 0.02);
}

TEST(PublicDecoratorTest, RaiseOnLimitFalse) {
    ratelimit::RateLimitDecorator d(1, 0.03, false);
    std::vector<int> track;
    auto fun = d.wrap([&track](){ track.push_back(track.size()+1); return track.back(); });
    EXPECT_EQ(fun(), 1);
    EXPECT_FALSE(static_cast<bool>(fun())); // None means zero/false
    std::this_thread::sleep_for(std::chrono::milliseconds(35));
    EXPECT_EQ(fun(), 2);
}