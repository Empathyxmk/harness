#include <gtest/gtest.h>
#include <cmath>
#include <vector>
#include "timer.h"

TEST(PublicTimerAdditional, ContextManagerRuns) {
    Timer timer("public_cmmsg", "Public elapsed: {0:.6f}s");
}

TEST(PublicTimerAdditional, StartStopElapsed) {
    Timer timer("public_simple", "Duration {0:.2f}");
    EXPECT_FALSE(timer._start_time.has_value());
    timer.start();
    EXPECT_TRUE(timer._start_time.has_value());
    timer.stop();
    double elapsed = timer.last();
    EXPECT_TRUE(std::isfinite(elapsed));
    EXPECT_GE(elapsed, 0.0);
}

TEST(PublicTimerAdditional, StrRepr) {
    Timer timer("public_simple", "Duration {0:.2f}");
    EXPECT_FALSE(timer.str().empty());
    EXPECT_NE(timer.repr().find("Timer"), std::string::npos);
}

TEST(PublicTimerAdditional, RunningStatusViaPrivate) {
    Timer timer("public_runstat", "Now running:{0}");
    timer.start();
    EXPECT_TRUE(timer._start_time.has_value());
    timer.stop();
    EXPECT_FALSE(timer._start_time.has_value());
}

TEST(PublicTimerAdditional, LoggerCallableText) {
    std::vector<std::string> messages;
    Timer timer("public_cbmsg", "", [&](const std::string& s){ messages.push_back(s); });
    timer.start();
    timer.stop();
    ASSERT_FALSE(messages.empty());
    EXPECT_NE(messages[0].find("Elapsed"), std::string::npos);
}

TEST(PublicTimerAdditional, WithoutTextLogger) {
    Timer timer("public_notext", "", nullptr);
    timer.start();
    timer.stop();
    SUCCEED();
}

TEST(PublicTimerAdditional, StopWithoutStartRaises) {
    Timer timer("public_exception", "fail fast");
    EXPECT_THROW(timer.stop(), TimerError);
}

TEST(PublicTimerAdditional, MultipleStartsRaises) {
    Timer timer("public_multi", "multi-case");
    timer.start();
    EXPECT_THROW(timer.start(), TimerError);
    timer.stop();
}

TEST(PublicTimerAdditional, LastWhenNan) {
    Timer timer("public_none", "noneCase");
    EXPECT_TRUE(std::isnan(timer.last()));
}

TEST(PublicTimerAdditional, CompareMultipleInstances) {
    Timer timer1("public_x");
    Timer timer2("public_y");
    EXPECT_NE(&timer1, &timer2);
}