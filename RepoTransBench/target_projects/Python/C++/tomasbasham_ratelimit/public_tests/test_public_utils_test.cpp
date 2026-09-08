#include <gtest/gtest.h>
#include <thread>
#include <chrono>
#include "ratelimit/utils.h"

TEST(PublicUtilsTest, NowTypeAndIncreasing) {
    double t1 = ratelimit::now()();
    std::this_thread::sleep_for(std::chrono::milliseconds(5));
    double t2 = ratelimit::now()();
    EXPECT_TRUE(typeid(t1)==typeid(double));
    EXPECT_GE(t2, t1);
}

TEST(PublicUtilsTest, NowMonotonic) {
    double v0 = ratelimit::now()();
    double v1 = ratelimit::now()();
    double v2 = ratelimit::now()();
    EXPECT_GE(v1, v0);
    EXPECT_GE(v2, v1);
}