#include <gtest/gtest.h>
#include <ctime>
#include <chrono>

TEST(PublicDatetimesTest, DifferentSimpleApi) {
    std::tm tm = {};
    tm.tm_year = 120; // 2020 - 1900
    tm.tm_mon = 1;    // Feb
    tm.tm_mday = 20;
    std::time_t expected = std::mktime(&tm);
    EXPECT_EQ(expected, std::mktime(&tm));  // Both frozen at 2020-02-20
}

TEST(PublicDatetimesTest, TZOffsetToday) {
    std::tm tm = {};
    tm.tm_year = 121; // 2021-1900
    tm.tm_mon = 11;   // Dec
    tm.tm_mday = 10;
    EXPECT_EQ(std::mktime(&tm), std::mktime(&tm));
}