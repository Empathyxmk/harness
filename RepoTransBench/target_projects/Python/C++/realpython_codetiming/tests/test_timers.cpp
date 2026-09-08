#include <gtest/gtest.h>
#include <cmath>
#include "timers.h"

TEST(Timers, AddAndTotalAndCount) {
    Timers timers;
    timers.add("t1", 1.0);
    timers.add("t1", 2.0);
    EXPECT_EQ(timers.count("t1"), 2);
    EXPECT_EQ(timers.total("t1"), 3.0);
}

TEST(Timers, MinMaxMeanMedianStdev) {
    Timers timers;
    std::vector<double> vals = {1.0, 2.0, 3.0};
    for (double v : vals)
        timers.add("x", v);
    EXPECT_EQ(timers.min("x"), *std::min_element(vals.begin(), vals.end()));
    EXPECT_EQ(timers.max("x"), *std::max_element(vals.begin(), vals.end()));
    EXPECT_DOUBLE_EQ(timers.mean("x"), (1.0+2.0+3.0)/3);
    EXPECT_DOUBLE_EQ(timers.median("x"), 2.0);
    EXPECT_TRUE(std::isfinite(timers.stdev("x")));
    EXPECT_GT(timers.stdev("x"), 0.0);
}

TEST(Timers, StdevNanForOneEntry) {
    Timers timers;
    timers.add("single", 2.345);
    EXPECT_TRUE(std::isnan(timers.stdev("single")));
}

TEST(Timers, ApplyKeyError) {
    Timers timers;
    EXPECT_THROW(timers.apply([](const std::vector<double>& x){ return std::accumulate(x.begin(), x.end(), 0.0); }, "not_exist"), std::out_of_range);
}

TEST(Timers, SetitemError) {
    Timers timers;
    EXPECT_THROW(timers["bad"] = 5.0, std::invalid_argument);
}

TEST(Timers, Clear) {
    Timers timers;
    timers.add("foo", 1.2);
    timers.clear();
    EXPECT_EQ(timers._timings.size(), 0);
    EXPECT_EQ(timers.data.size(), 0);
}

TEST(Timers, TotalNoTimings) {
    Timers timers;
    EXPECT_THROW(timers.total("missing"), std::out_of_range);
}

TEST(Timers, MinMaxZeroIfEmpty) {
    Timers timers;
    timers._timings["e"] = {};
    EXPECT_EQ(timers.min("e"), 0.0);
    EXPECT_EQ(timers.max("e"), 0.0);
}

TEST(Timers, MeanMedianZeroIfEmpty) {
    Timers timers;
    timers._timings["e"] = {};
    EXPECT_EQ(timers.mean("e"), 0.0);
    EXPECT_EQ(timers.median("e"), 0.0);
}

TEST(Timers, StdevKeyErrorIfMissing) {
    Timers timers;
    EXPECT_THROW(timers.stdev("N/A"), std::out_of_range);
}