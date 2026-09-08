#include <gtest/gtest.h>
#include "sparts/counters.h"
#include <vector>
#include <string>
#include <cmath>

using namespace sparts;

TEST(PublicCounters, Sum) {
    Sum c;
    EXPECT_DOUBLE_EQ(c(), 0.0);
    c.incrementBy(3);
    EXPECT_DOUBLE_EQ(c(), 3.0);
    c.increment();
    EXPECT_DOUBLE_EQ(c(), 4.0);
    c.add(6);
    EXPECT_DOUBLE_EQ(c(), 10.0);

    EXPECT_EQ((int)c, 10);
    EXPECT_DOUBLE_EQ((double)c, 10.0);
    EXPECT_EQ((std::string)c, "10.000000");

    c.reset(5.5);
    EXPECT_DOUBLE_EQ((double)c, 5.5);
}

TEST(PublicCounters, Count) {
    Count c;
    EXPECT_EQ(c(), 0);
    c.add(55);
    EXPECT_EQ(c(), 1);
}

TEST(PublicCounters, Max) {
    Max c;
    EXPECT_FALSE(c().has_value());
    c.add(5);
    ASSERT_TRUE(c().has_value());
    EXPECT_EQ(*c(), 5);
    c.add(-15);
    EXPECT_EQ(*c(), 5);
    c.add(15);
    EXPECT_EQ(*c(), 15);
}

TEST(PublicCounters, Min) {
    Min c;
    EXPECT_FALSE(c().has_value());
    c.add(5);
    ASSERT_TRUE(c().has_value());
    EXPECT_EQ(*c(), 5);
    c.add(-15);
    EXPECT_EQ(*c(), -15);
    c.add(2);
    EXPECT_EQ(*c(), -15);
}

TEST(PublicCounters, Average) {
    Average c;
    EXPECT_FALSE(c().has_value());
    c.add(20);
    c.add(40);
    ASSERT_TRUE(c().has_value());
    EXPECT_EQ(*c(), 30.0);
}

TEST(PublicCounters, CallbackCounter) {
    double l[1] = {42.0};
    CallbackCounter c([&l]() { return l[0]; });
    EXPECT_DOUBLE_EQ(c(), 42.0);
    l[0] = 7.0;
    EXPECT_DOUBLE_EQ(c(), 7.0);
}

TEST(PublicCounters, SampleNames) {
    Samples c = samples("bar", {SampleType::SUM}, {50});
    c.add(10);
    EXPECT_EQ(c.getCounter("bar.sum.50"), 10);

    Samples c2 = samples("", {SampleType::SUM}, {50});
    c2.add(3);
    EXPECT_EQ(c2.getCounter("sum.50"), 3);
}

/* Windowed sample test would need time control as in the Python (monkeypatch).
   Our C++ code does not support it yet, skipping direct translation, see original.
*/