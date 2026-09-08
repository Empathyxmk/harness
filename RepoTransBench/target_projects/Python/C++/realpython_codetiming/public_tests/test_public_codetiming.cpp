#include <gtest/gtest.h>
#include <cmath>
#include <string>
#include <thread>
#include <chrono>
#include "timer.h"

namespace {
const char* USER_TIME_PREFIX = "Time spent:";
const char* USER_TIME_MESSAGE = "Time spent: {0:.5f} s";

// Simulate Python's waste_custom_time
void waste_custom_time(int num=500) {
    volatile int sum = 0;
    for (int n=0; n<num; ++n)
        sum += (n + 1);
}

struct MyLogger {
    std::string logs;
    void operator()(const std::string& msg) { logs += msg; }
};

}

TEST(PublicCodetiming, TimerAsDecorator) {
    Timer t("public", USER_TIME_MESSAGE);
    t.start();
    waste_custom_time();
    t.stop();
    EXPECT_TRUE(t.last() >= 0.0);
}

TEST(PublicCodetiming, TimerAsContextManager) {
    Timer t("public_ctx", USER_TIME_MESSAGE);
    t.start();
    waste_custom_time();
    t.stop();
    EXPECT_TRUE(t.last() >= 0.0);
}

TEST(PublicCodetiming, ExplicitTimer) {
    Timer t("explicit", USER_TIME_MESSAGE);
    t.start();
    waste_custom_time();
    t.stop();
    EXPECT_TRUE(std::isfinite(t.last()));
}

TEST(PublicCodetiming, ErrorIfTimerNotRunning) {
    Timer t("explicit", USER_TIME_MESSAGE);
    EXPECT_THROW(t.stop(), TimerError);
}

TEST(PublicCodetiming, AccessTimerObjectInContext) {
    Timer t("access_ctx", USER_TIME_MESSAGE);
    t.start();
    EXPECT_EQ(t.textTemplate().find(USER_TIME_PREFIX), 0u);
    t.stop();
}

TEST(PublicCodetiming, CustomLogger) {
    MyLogger logger;
    Timer t("logcustom", USER_TIME_MESSAGE, std::ref(logger));
    t.start();
    waste_custom_time();
    t.stop();
    EXPECT_FALSE(logger.logs.empty());
}

TEST(PublicCodetiming, TimerWithoutText) {
    Timer t("nooutput", "", nullptr);
    t.start();
    waste_custom_time();
    t.stop();
    SUCCEED();
}

TEST(PublicCodetiming, AccumulatedDecorator) {
    Timer t("bucket", USER_TIME_MESSAGE);
    t.start();
    waste_custom_time();
    t.stop();
    t.start();
    waste_custom_time();
    t.stop();
    EXPECT_TRUE(t.last() >= 0.0);
}

TEST(PublicCodetiming, ErrorIfRestartingRunningTimer) {
    Timer t("restart", USER_TIME_MESSAGE);
    t.start();
    EXPECT_THROW(t.start(), TimerError);
    t.stop();
}

TEST(PublicCodetiming, LastStartsAsNan) {
    Timer t;
    EXPECT_TRUE(std::isnan(t.last()));
}

TEST(PublicCodetiming, TimerSetsLast) {
    Timer t("wait", "", nullptr);
    t.start();
    std::this_thread::sleep_for(std::chrono::milliseconds(10));
    t.stop();
    EXPECT_GE(t.last(), 0.01);
}