#include <gtest/gtest.h>
#include <thread>
#include <chrono>
#include "ratelimit/decorators.h"

TEST(DecoratorsEdgeCases, ClampedCallsMinAndMax) {
    ratelimit::RateLimitDecorator d(-9, 1, nullptr);
    EXPECT_EQ(d.clamped_calls, 1);

    ratelimit::RateLimitDecorator d2(
        (int64_t)std::numeric_limits<int64_t>::max() + 123456, 1, nullptr);
    EXPECT_EQ(d2.clamped_calls, std::numeric_limits<int64_t>::max());
}

TEST(DecoratorsEdgeCases, DecoratorThreadSafety) {
    ratelimit::RateLimitDecorator dec(2, 1, nullptr);

    std::vector<int> result;
    auto foo = dec.wrap([&result](int x) {
        result.push_back(x);
        return x;
    });

    std::thread t1([&]() { foo(1); });
    std::thread t2([&]() { foo(2); });
    t1.join();
    t2.join();
    std::sort(result.begin(), result.end());
    EXPECT_EQ(result, (std::vector<int>{1, 2}));
}

TEST(DecoratorsEdgeCases, PeriodRemainingZero) {
    int last_reset = 15;
    auto fake_clock = []() { return 20.0; };
    ratelimit::RateLimitDecorator dec(2, 5, fake_clock);
    dec.last_reset = 15;
    std::vector<std::string> called;
    auto f = dec.wrap([&]() {
        called.push_back("called");
        return 123;
    });
    EXPECT_EQ(f(), 123);
    EXPECT_EQ(f(), 123);
}

TEST(DecoratorsEdgeCases, PeriodRemainingNegative) {
    struct State { int t = 0; } state;
    auto fake_clock = [&state]() {
        int val = state.t;
        state.t += 100;
        return val;
    };
    ratelimit::RateLimitDecorator dec(1, 1, fake_clock);

    std::vector<int> called;
    auto foo = dec.wrap([&called]() {
        called.push_back(1);
    });
    foo();
    foo();
    EXPECT_EQ(called.size(), 2);
}