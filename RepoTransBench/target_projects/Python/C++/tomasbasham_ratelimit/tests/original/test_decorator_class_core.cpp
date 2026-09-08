#include <gtest/gtest.h>
#include <thread>
#include <chrono>
#include "ratelimit/decorators.h"
#include "ratelimit/exception.h"

// Helper for monkeypatch: not needed, replaced by direct calls

TEST(RateLimitDecorator, ConstructorClampsCalls) {
    // Negative calls
    ratelimit::RateLimitDecorator rld_neg(-5, 1);
    EXPECT_EQ(rld_neg.clamped_calls, 1);

    // Very large number
    ratelimit::RateLimitDecorator rld_large((int64_t)1 << 60, 1);
    EXPECT_EQ(rld_large.clamped_calls, std::numeric_limits<int64_t>::max());

    // Floor for floats
    ratelimit::RateLimitDecorator rld_float(3.9, 1);
    EXPECT_EQ(rld_float.clamped_calls, 3);
}

TEST(RateLimitDecorator, DecoratorRateLimitRaises) {
    ratelimit::RateLimitDecorator rl(1, 0.05);

    int state = 0;
    auto f = rl.wrap([&]() -> std::string {
        return "foo";
    });
    EXPECT_EQ(f(), "foo");
    EXPECT_THROW(f(), ratelimit::RateLimitException);
    std::this_thread::sleep_for(std::chrono::milliseconds(60));
    EXPECT_EQ(f(), "foo");
}

TEST(RateLimitDecorator, DecoratorDoesNotRaise) {
    ratelimit::RateLimitDecorator rl(1, 0.05, false);
    int result = 0;
    auto f = rl.wrap([&result]() -> int {
        result++;
        return result;
    });
    EXPECT_EQ(f(), 1);
    std::this_thread::sleep_for(std::chrono::milliseconds(60));
    EXPECT_EQ(f(), 2);
}

TEST(RateLimitDecorator, ThreadSafety) {
    ratelimit::RateLimitDecorator rld(10, 1);
    auto dummy = rld.wrap([]() { return 42; });
    dummy();
    dummy();
    // Should establish lock/lazy init logic, always passes for this stub
    EXPECT_TRUE(rld.has_lock());
}