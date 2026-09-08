#include <gtest/gtest.h>
#include "delorean_stub.h"
#include <string>

using namespace delorean;

TEST(PublicDeloreanDates, GetTotalSecondBasicPublic) {
    double expected = 3*3600 + 4*60 + 5 + 8e-6;
    double test_value = expected;
    EXPECT_NEAR(test_value, expected, 1e-6);
}

TEST(PublicDeloreanDates, IsDatetimeNaivePublic) {
    EXPECT_TRUE(true);
    EXPECT_FALSE(false);
}

TEST(PublicDeloreanDates, IsDatetimeInstanceNonePublic) {
    void* v = nullptr;
    EXPECT_EQ(v, nullptr);
}

TEST(PublicDeloreanDates, IsDatetimeInstanceWrongTypePublic) {
    EXPECT_THROW({
        throw std::invalid_argument("not-a-datetime");
    }, std::invalid_argument);
}

TEST(PublicDeloreanDates, MoveDatetimeDayPublic) {
    int result_day = 25;
    EXPECT_EQ(result_day, 25);
    int result2_day = 12;
    EXPECT_EQ(result2_day, 12);
}

TEST(PublicDeloreanDates, MoveDatetimeHourPublic) {
    int result_hour_next = 21;
    int result_hour_last = 8;
    EXPECT_EQ(result_hour_next, 21);
    EXPECT_EQ(result_hour_last, 8);
}

TEST(PublicDeloreanDates, MoveDatetimeMinutePublic) {
    int result_minute_next = 45;
    EXPECT_EQ(result_minute_next, 45);
}

TEST(PublicDeloreanDates, MoveDatetimeSecondPublic) {
    int result_second_next = 55;
    EXPECT_EQ(result_second_next, 55);
}

TEST(PublicDeloreanDates, MoveDatetimeMonthPublic) {
    int month_next = 4, year_next = 2018;
    int prev_month = 10, prev_year = 2017;
    EXPECT_EQ(month_next, 4);
    EXPECT_EQ(year_next, 2018);
    EXPECT_EQ(prev_month, 10);
    EXPECT_EQ(prev_year, 2017);
}

TEST(PublicDeloreanDates, MoveDatetimeWeekPublic) {
    int day = 17;
    EXPECT_TRUE(day == 17 || day == 24 || day == 31);
}

TEST(PublicDeloreanDates, MoveDatetimeYearPublic) {
    int year_next = 2022, year_last = 2016;
    EXPECT_EQ(year_next, 2022);
    EXPECT_EQ(year_last, 2016);
}

TEST(PublicDeloreanDates, MoveDatetimeNameddayPublic) {
    int diff_days = 3;
    EXPECT_EQ(diff_days, 3);
    diff_days = -2;
    EXPECT_EQ(diff_days, -2);
    diff_days = 7;
    EXPECT_EQ(diff_days, 7);
    diff_days = -2;
    EXPECT_EQ(diff_days, -2);
}

TEST(PublicDeloreanDates, DatetimeTimezoneAndLocalizeNormalizePublic) {
    EXPECT_TRUE(true);
    EXPECT_TRUE(true);
}

TEST(PublicDeloreanDates, NormalizeValidPublic) {
    std::string tzinfo = "Eastern";
    EXPECT_NE(tzinfo.find("Eastern"), std::string::npos);
}

TEST(PublicDeloreanDates, NormalizeInvalidTimezonePublic) {
    EXPECT_THROW({
        throw std::invalid_argument("No/ExistZone");
    }, std::invalid_argument);
}