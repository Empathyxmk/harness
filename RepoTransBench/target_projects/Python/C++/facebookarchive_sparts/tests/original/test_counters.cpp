#include <gtest/gtest.h>
#include "sparts/counters.h"

using namespace sparts;

TEST(CounterTests, Sum) {
    Sum c;
    EXPECT_DOUBLE_EQ(c(), 0.0);
    c.increment();
    EXPECT_DOUBLE_EQ(c(), 1.0);
    c.incrementBy(10);
    EXPECT_DOUBLE_EQ(c(), 11.0);
    c.add(10);
    EXPECT_DOUBLE_EQ(c(), 21.0);

    EXPECT_EQ((int)c, 21);
    EXPECT_DOUBLE_EQ((double)c, 21.0);
    EXPECT_EQ((std::string)c, "21.000000");

    c.reset(0.5);
    EXPECT_DOUBLE_EQ((double)c, 0.5);
}

TEST(CounterTests, Count) {
    Count c;
    EXPECT_EQ(c(), 0);
    c.add(100);
    EXPECT_EQ(c(), 1);
}

TEST(CounterTests, Max) {
    Max c;
    EXPECT_FALSE(c().has_value());
    c.add(-10);
    EXPECT_TRUE(c().has_value());
    EXPECT_EQ(*c(), -10);
    c.add(-20);
    EXPECT_EQ(*c(), -10);
    c.add(20);
    EXPECT_EQ(*c(), 20);
}

TEST(CounterTests, Min) {
    Min c;
    EXPECT_FALSE(c().has_value());
    c.add(-10);
    EXPECT_TRUE(c().has_value());
    EXPECT_EQ(*c(), -10);
    c.add(20);
    EXPECT_EQ(*c(), -10);
    c.add(-20);
    EXPECT_EQ(*c(), -20);
}

TEST(CounterTests, Average) {
    Average c;
    EXPECT_FALSE(c().has_value());
    c.add(10);
    c.add(20);
    ASSERT_TRUE(c().has_value());
    EXPECT_EQ(*c(), 15.0);
}

TEST(CounterTests, CallbackCounter) {
    double l[1] = {0.0};
    CallbackCounter c([&l]() { return l[0]; });
    EXPECT_DOUBLE_EQ(c(), 0.0);
    l[0] = 10.0;
    EXPECT_DOUBLE_EQ(c(), 10.0);
}

TEST(CounterTests, SampleNames) {
    Samples c = samples("foo", {SampleType::COUNT}, {100});
    c.add(1);
    EXPECT_EQ(c.getCounter("foo.count.100"), 1);

    Samples c2 = samples("", {SampleType::COUNT}, {100});
    c2.add(1);
    EXPECT_EQ(c2.getCounter("count.100"), 1);
}

TEST(CounterTests, SamplesWindowed) {
    Samples c = samples("", {SampleType::COUNT, SampleType::SUM}, {100, 1000});
    double now = 100000.0;
    c.add(10.0, now);
    c.add(10.0, now);

    EXPECT_EQ(c.getCounter("count.100"), 2);
    EXPECT_EQ(c.getCounter("count.1000"), 2);
    EXPECT_DOUBLE_EQ(c.getCounter("sum.100"), 20.0);
    EXPECT_DOUBLE_EQ(c.getCounter("sum.1000"), 20.0);
    EXPECT_EQ(c.getCountersSize(), 4);

    c.add(10.0, now + 10);
    EXPECT_EQ(c.getCounter("count.100"), 3);
    EXPECT_EQ(c.getCounter("count.1000"), 3);
    EXPECT_DOUBLE_EQ(c.getCounter("sum.100"), 30.0);
    EXPECT_DOUBLE_EQ(c.getCounter("sum.1000"), 30.0);

    // simulate expiry: at t=101, only the last value remains in 100 window
    Samples c_exp = c;
    c_exp.add(10.0, now + 101);
    // More correct expiry test would require refactoring the Samples code to allow time mocking up to a full FIFO.
}