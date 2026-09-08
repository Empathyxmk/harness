#include <gtest/gtest.h>
#include <thread>
#include <chrono>
#include "ratelimit/utils.h"

TEST(PublicUtilsAdditional, NowMonotonicity) {
    double t1 = ratelimit::now()();
    std::this_thread::sleep_for(std::chrono::milliseconds(10));
    double t2 = ratelimit::now()();
    EXPECT_GE(t2, t1);
}

TEST(PublicUtilsAdditional, NowCloseToSystemTime) {
    double t1 = ratelimit::now()();
    double t2 = ratelimit::system_time();
    EXPECT_LT(std::abs(t2-t1), 1.0);
}