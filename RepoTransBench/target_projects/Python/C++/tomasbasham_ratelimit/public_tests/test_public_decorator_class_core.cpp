#include <gtest/gtest.h>
#include <limits>
#include <thread>
#include <chrono>
#include "ratelimit/decorators.h"
#include "ratelimit/exception.h"

TEST(PublicDecoratorClassCore, ConstructorClampsCalls) {
    ratelimit::RateLimitDecorator rld0(0, 2);
    EXPECT_EQ(rld0.clamped_calls, 1);
    ratelimit::RateLimitDecorator rld_big((int64_t)std::numeric_limits<int64_t>::max() + 100, 2);
    EXPECT_EQ(rld_big.clamped_calls, std::numeric_limits<int64_t>::max());
    ratelimit::RateLimitDecorator rld_float(7.8, 2);
    EXPECT_EQ(rld_float.clamped_calls, 7);
}

TEST(PublicDecoratorClassCore, DecoratorRateLimitRaises) {
    ratelimit::RateLimitDecorator rl(2, 0.03);
    int call_no = 0;
    auto foo = rl.wrap([&call_no]() { call_no++; return std::string("bar"); });
    EXPECT_EQ(foo(), "bar");
    EXPECT_EQ(foo(), "bar");
    EXPECT_THROW(foo(), ratelimit::RateLimitException);
    std::this_thread::sleep_for(std::chrono::milliseconds(35));
    EXPECT_EQ(foo(), "bar");
}

TEST(PublicDecoratorClassCore, DecoratorDoesNotRaise) {
    ratelimit::RateLimitDecorator rl(2, 0.04, false);
    std::vector<char> result;
    auto bar = rl.wrap([&result](){ result.push_back('x'); return (int)result.size(); });
    EXPECT_EQ(bar(), 1);
    EXPECT_EQ(bar(), 2);
    std::this_thread::sleep_for(std::chrono::milliseconds(45));
    EXPECT_EQ(bar(), 3);
}

TEST(PublicDecoratorClassCore, ThreadSafety) {
    ratelimit::RateLimitDecorator rld(4, 1);
    auto dummy2 = rld.wrap([]() { return 24; });
    dummy2();
    dummy2();
    dummy2();
    EXPECT_TRUE(rld.has_lock());
}