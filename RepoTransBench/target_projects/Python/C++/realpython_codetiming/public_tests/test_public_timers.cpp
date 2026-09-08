#include <gtest/gtest.h>
#include <cmath>
#include "timers.h"

TEST(PublicTimers, AddAndTotalAndCount) {
    Timers timers;
    timers.add("alpha", 0.5);
    timers.add("alpha", 0.7);
    EXPECT_EQ(timers.count("alpha"), 2);
    EXPECT_DOUBLE_EQ(timers.total("alpha"), 1.2);
}

TEST(PublicTimers, MinMaxMeanMedianStdev) {
    Timers timers;
    std::vector<double> vals = {4.0, 5.5, 6.5};
    for (double v : vals)
        timers.add("y", v);
    EXPECT_EQ(timers.min("y"), *std::min_element(vals.begin(), vals.end()));
    EXPECT_EQ(timers.max("y"), *std::max_element(vals.begin(), vals.end()));
    EXPECT_DOUBLE_EQ(timers.mean("y"), (4.0+5.5+6.5)/3);
    EXPECT_DOUBLE_EQ(timers.median("y"), 5.5);
    EXPECT_TRUE(std::isfinite(timers.stdev("y")));
    EXPECT_GT(timers.stdev("y"), 0.0);
}

TEST(PublicTimers, StdevNanForOneEntry) {
    Timers timers;
    timers.add("single_public", 13.6);
    EXPECT_TRUE(std::isnan(timers.stdev("single_public")));
}

TEST(PublicTimers, ApplyKeyError) {
    Timers timers;
    EXPECT_THROW(timers.apply([](const std::vector<double>& x){ return std::accumulate(x.begin(), x.end(), 0.0); }, "does_not_exist"), std::out_of_range);
}

TEST(PublicTimers, SetitemError) {
    Timers timers;
    EXPECT_THROW(timers["forbidden"] = 3.14, std::invalid_argument);
}

TEST(PublicTimers, Clear) {
    Timers timers;
    timers.add("bar", 2.4);
    timers.clear();
    EXPECT_EQ(timers._timings.size(), 0);
    EXPECT_EQ(timers.data.size(), 0);
}

TEST(PublicTimers, TotalNoTimings) {
    Timers timers;
    EXPECT_THROW(timers.total("ghost"), std::out_of_range);
}

TEST(PublicTimers, MinMaxZeroIfEmpty) {
    Timers timers;
    timers._timings["emptycase"] = {};
    EXPECT_EQ(timers.min("emptycase"), 0.0);
    EXPECT_EQ(timers.max("emptycase"), 0.0);
}

TEST(PublicTimers, MeanMedianZeroIfEmpty) {
    Timers timers;
    timers._timings["emptycase"] = {};
    EXPECT_EQ(timers.mean("emptycase"), 0.0);
    EXPECT_EQ(timers.median("emptycase"), 0.0);
}

TEST(PublicTimers, StdevKeyErrorIfMissing) {
    Timers timers;
    EXPECT_THROW(timers.stdev("MISSING"), std::out_of_range);
}