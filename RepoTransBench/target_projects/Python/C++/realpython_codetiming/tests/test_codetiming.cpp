#include <gtest/gtest.h>
#include <cmath>
#include <sstream>
#include <chrono>
#include <thread>
#include "timer.h"
#include "timers.h"

// Simulate Python's waste_time logic
double waste_time(int num = 1000) {
    double s = 0;
    for (int n=0; n<num; ++n) s += n*n;
    return s;
}

TEST(Codetiming, TimerStartStopElapsed) {
    Timer t("test", "Test {0:.4f}");
    t.start();
    waste_time();
    double e = t.stop();
    EXPECT_TRUE(e >= 0.0);
    EXPECT_TRUE(std::isfinite(t.last()));
}

TEST(Codetiming, TimerStartStopThrow) {
    Timer t("test", "Test {0:.4f}");
    EXPECT_THROW(t.stop(), TimerError);
}

TEST(Codetiming, TimerMultipleStartsThrow) {
    Timer t("test", "Test {0:.4f}");
    t.start();
    EXPECT_THROW(t.start(), TimerError);
    t.stop();
}

TEST(Codetiming, TimerLastStartsAsNan) {
    Timer t;
    EXPECT_TRUE(std::isnan(t.last()));
}

TEST(Codetiming, TimerSetsLastAfterSleep) {
    Timer t("sleep", "", nullptr);
    t.start();
    std::this_thread::sleep_for(std::chrono::milliseconds(20));
    t.stop();
    EXPECT_GE(t.last(), 0.02);
}

TEST(Codetiming, TimerStrRepr) {
    Timer t("checkrepr");
    EXPECT_NE(t.str().find("Timer"), std::string::npos);
    EXPECT_NE(t.repr().find("Timer"), std::string::npos);
}

TEST(Codetiming, CompareMultipleInstances) {
    Timer timer1("a");
    Timer timer2("b");
    EXPECT_NE(&timer1, &timer2);
}