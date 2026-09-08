#include <gtest/gtest.h>
#include <cmath>
#include <vector>
#include "timer.h"

TEST(TimerAdditional, ContextManagerRuns) {
    Timer timer("cmmsg", "Elapsed time: {0:.4f}s");
    // Context manager is RAII in C++
    // Just construct & destruct
}

TEST(TimerAdditional, StartStopElapsed) {
    Timer timer("simple", "Time {0:.4f}");
    EXPECT_FALSE(timer._start_time.has_value());
    timer.start();
    EXPECT_TRUE(timer._start_time.has_value());
    timer.stop();
    double elapsed = timer.last();
    EXPECT_TRUE(std::isfinite(elapsed));
}

TEST(TimerAdditional, StrRepr) {
    Timer timer("simple", "Time {0:.4f}");
    EXPECT_FALSE(timer.str().empty());
    EXPECT_NE(timer.repr().find("Timer"), std::string::npos);
}

TEST(TimerAdditional, RunningStatusViaPrivate) {
    Timer timer("runstat", "Running:{0}");
    timer.start();
    EXPECT_TRUE(timer._start_time.has_value());
    timer.stop();
    EXPECT_FALSE(timer._start_time.has_value());
}

TEST(TimerAdditional, LoggerCallableText) {
    std::vector<std::string> messages;
    Timer timer("cbmsg", "", [&](const std::string& s){ messages.push_back(s); });
    timer.start();
    timer.stop();
    ASSERT_FALSE(messages.empty());
    EXPECT_NE(messages[0].find("Elapsed"), std::string::npos);
}

TEST(TimerAdditional, WithoutTextLogger) {
    Timer timer("notext", "", nullptr);
    timer.start();
    timer.stop();
    // Should not log or throw
    SUCCEED();
}

TEST(TimerAdditional, StopWithoutStartRaises) {
    Timer timer("exception", "fail");
    EXPECT_THROW(timer.stop(), TimerError);
}

TEST(TimerAdditional, MultipleStartsRaises) {
    Timer timer("multi", "multi");
    timer.start();
    EXPECT_THROW(timer.start(), TimerError);
    timer.stop();
}

TEST(TimerAdditional, LastWhenNan) {
    Timer timer("none", "none");
    EXPECT_TRUE(std::isnan(timer.last()));
}

TEST(TimerAdditional, CompareMultipleInstances) {
    Timer timer1("a");
    Timer timer2("b");
    EXPECT_NE(&timer1, &timer2);
}