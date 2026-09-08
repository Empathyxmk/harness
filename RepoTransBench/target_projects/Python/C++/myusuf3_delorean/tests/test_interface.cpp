#include <gtest/gtest.h>
#include "delorean_stub.h"
#include <stdexcept>
#include <string>
#include <memory>

using namespace delorean;

TEST(DeloreanInterfaceTest, ConstructorNaive) {
    Delorean d(2022, 1, 2, 12, 0, 0, "UTC");
    EXPECT_EQ(d.datetime.year, 2022);
    EXPECT_EQ(d.datetime.month, 1);
    EXPECT_EQ(d.datetime.day, 2);
    EXPECT_EQ(d.datetime.hour, 12);
    EXPECT_EQ(d.tz.zone, "UTC");
}

TEST(DeloreanInterfaceTest, ConstructorTimezoneStrAndObj) {
    Delorean d1(2022, 1, 2, 13, 0, 0, "US/Pacific");
    EXPECT_EQ(d1.tz.zone, "US/Pacific");
    Delorean d2(2022, 1, 2, 13, 0, 0, "US/Eastern");
    EXPECT_EQ(d2.tz.zone, "US/Eastern");
}

TEST(DeloreanInterfaceTest, ConstructorInvalidTimezone) {
    EXPECT_THROW({
        Delorean d(2022, 1, 2, 13, 0, 0, "Invalid/Zone");
    }, DeloreanInvalidTimezone);
}

TEST(DeloreanInterfaceTest, ShiftMinutesAndSeconds) {
    Delorean d(2017, 5, 6, 12, 30, 0, "UTC");
    Delorean d2 = d.shift(0, 2, 5);
    EXPECT_EQ(d2.datetime.minute, 32);
    EXPECT_EQ(d2.datetime.second, 5);
}

TEST(DeloreanInterfaceTest, NextLastMethods) {
    Delorean d(2021, 12, 31, 23, 0, 0, "UTC");
    Delorean next_day = d.next_day();
    EXPECT_TRUE(next_day.datetime.day == 1 || next_day.datetime.month == 1);

    Delorean last_week = d.last_week();
    int diff_days = d.days_between(last_week);
    EXPECT_TRUE(diff_days >= 0 && diff_days <= 7);
}

TEST(DeloreanInterfaceTest, TruncateToDay) {
    Delorean d(2022, 3, 4, 15, 34, 56, "UTC");
    Delorean truncated = d.truncate("day");
    EXPECT_EQ(truncated.datetime.hour, 0);
    EXPECT_EQ(truncated.datetime.minute, 0);
}

TEST(DeloreanInterfaceTest, EqAndRepr) {
    Delorean d1(2022, 3, 4, 0, 0, 0, "UTC");
    Delorean d2(2022, 3, 4, 0, 0, 0, "UTC");
    EXPECT_TRUE(d1 == d2);

    EXPECT_NE(d1.repr().find("Delorean"), std::string::npos);
}

TEST(DeloreanInterfaceTest, RollforwardRollbackUp) {
    Delorean d(2022, 3, 6, 0, 0, 0, "UTC");
    Delorean rf = d.rollforward("Monday");
    Delorean rb = d.rollback("Monday");
    EXPECT_TRUE(rf.has_attr_datetime());
    EXPECT_TRUE(rb.has_attr_datetime());
    EXPECT_TRUE(rf != d || rb != d); // could land on the same
}

TEST(DeloreanInterfaceTest, TimezoneAndConvert) {
    Delorean d(2021, 3, 1, 10, 0, 0, "UTC");
    Delorean local = d.localize("US/Pacific");
    EXPECT_EQ(local.tz.zone, "US/Pacific");
    Delorean norm = d.normalize("US/Pacific");
    EXPECT_EQ(norm.tz.zone, "US/Pacific");
    EXPECT_TRUE(typeid(d.to_unix()) == typeid(double));
    EXPECT_TRUE(d.to_pytz().has_tzinfo());
    EXPECT_TRUE(d.to_datetime().has_tzinfo());
}

TEST(DeloreanInterfaceTest, ConvertUnsupported) {
    Delorean d(2022, 1, 1, 0, 0, 0, "UTC");
    EXPECT_THROW({
        d.truncate("unknown");
    }, std::invalid_argument);
}

TEST(DeloreanInterfaceTest, FactoryMethods) {
    Delorean d1 = Delorean::utcnow();
    Delorean d2 = Delorean::now("UTC");
    Delorean d3 = Delorean::parse("2021-01-01T10:00:00Z");
    Delorean d4 = Delorean::epoch(0, "UTC");
    EXPECT_EQ(d4.datetime.year, 1970);

    EXPECT_TRUE(typeid(d1) == typeid(Delorean));
    EXPECT_TRUE(typeid(d2) == typeid(Delorean));
    EXPECT_TRUE(typeid(d3) == typeid(Delorean));
    EXPECT_TRUE(typeid(d4) == typeid(Delorean));
}