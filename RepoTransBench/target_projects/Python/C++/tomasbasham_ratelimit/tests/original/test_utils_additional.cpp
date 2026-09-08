#include <gtest/gtest.h>
#include <thread>
#include <chrono>
#include "ratelimit/utils.h"

TEST(UtilsAdditional, NowReturnsMonotonicOrTime) {
    auto func = ratelimit::now();
    double t1 = func();
    std::this_thread::sleep_for(std::chrono::milliseconds(10));
    double t2 = func();
    EXPECT_GT(t2, t1);

    // Simulate no monotonic present: mock by forcing fallback
    auto fallback_func = ratelimit::now(/*force_time*/true);
    double f1 = fallback_func();
    std::this_thread::sleep_for(std::chrono::milliseconds(10));
    double f2 = fallback_func();
    EXPECT_GT(f2, f1);
}