#include <gtest/gtest.h>
#include <thread>
#include <chrono>
#include "ratelimit/decorators.h"
#include "ratelimit/exception.h"

namespace {
int dummy_clock_val = 1000;
int dummy_clock() { return dummy_clock_val++; }
}

TEST(DecoratorDecoratorTests, AllowsCallsWithinLimit) {
    std::vector<int> calls;
    auto clock = dummy_clock;
    ratelimit::RateLimitDecorator dec(2, 10, clock);
    auto func = dec.wrap([&calls](int x) { 
        calls.push_back(x); 
        return x; 
    });
    EXPECT_EQ(func(2), 2);
    EXPECT_EQ(func(3), 3);
    EXPECT_EQ(calls, std::vector<int>({2,3}));
}

TEST(DecoratorDecoratorTests, RaisesOnExceedingLimit) {
    dummy_clock_val = 1000;
    ratelimit::RateLimitDecorator dec(1, 10, dummy_clock, true);
    std::vector<int> decorated_calls;
    auto func = dec.wrap([&decorated_calls](int x) {
        decorated_calls.push_back(x);
        return x;
    });
    func(1);
    EXPECT_THROW(func(2), ratelimit::RateLimitException);
}

TEST(DecoratorDecoratorTests, ReturnsNoneWhenRaiseOnLimitFalse) {
    dummy_clock_val = 1000;
    ratelimit::RateLimitDecorator dec(1, 10, dummy_clock, false);
    std::vector<int> calls;
    auto func = dec.wrap([&calls](int x) {
        calls.push_back(x);
        return x;
    });
    EXPECT_EQ(func(5), 5);
    EXPECT_FALSE(func(6)); // returns 0 or nullptr
    EXPECT_EQ(calls, std::vector<int>({5}));
}

TEST(DecoratorDecoratorTests, ResetsAfterPeriod) {
    // Simulate resetting: period short, clock increments per call
    static double t = 0.0;
    auto fake_clock = []() -> double { double out = t; t += 0.1; return out; };
    ratelimit::RateLimitDecorator dec(1, 0.05, fake_clock);
    auto f = dec.wrap([](int x){ return x; });
    EXPECT_EQ(f(1), 1);
    EXPECT_EQ(f(2), 2);
}

TEST(DecoratorDecoratorTests, PeriodRemainingReturnsProperValue) {
    struct { double t = 505; double reset = 498; } state;
    auto fake_clock = [&state]() { return state.t; };
    ratelimit::RateLimitDecorator dec(1, 10, fake_clock);
    dec.last_reset = state.reset;
    double remaining = dec.period_remaining();
    EXPECT_EQ(remaining, 3);
}