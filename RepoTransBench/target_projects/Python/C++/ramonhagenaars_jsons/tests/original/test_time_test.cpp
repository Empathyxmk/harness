#include <gtest/gtest.h>
#include <ctime>
#include <string>

// Converts a struct tm to 'HH:MM:SS'
std::string time_to_str(const std::tm& tm) {
    char buf[12];
    std::strftime(buf, sizeof(buf), "%H:%M:%S", &tm);
    return std::string(buf);
}

// Converts 'HH:MM:SS' to struct tm (day/month/year/other fields ignored)
std::tm str_to_time(const std::string& s) {
    std::tm tm{};
    sscanf(s.c_str(), "%2d:%2d:%2d", &tm.tm_hour, &tm.tm_min, &tm.tm_sec);
    return tm;
}

class JsonsTimeTest : public ::testing::Test {};

TEST_F(JsonsTimeTest, test_dump_time) {
    std::tm tm = {};
    tm.tm_year = 2018 - 1900;
    tm.tm_mon = 7 - 1;
    tm.tm_mday = 8;
    tm.tm_hour = 21;
    tm.tm_min = 34;
    tm.tm_sec = 0;
    std::string dumped = time_to_str(tm);
    EXPECT_EQ(dumped, "21:34:00");
}

TEST_F(JsonsTimeTest, test_load_time) {
    std::string s = "21:34:00";
    std::tm expected{};
    expected.tm_hour = 21;
    expected.tm_min = 34;
    expected.tm_sec = 0;
    std::tm loaded = str_to_time(s);
    EXPECT_EQ(loaded.tm_hour, expected.tm_hour);
    EXPECT_EQ(loaded.tm_min, expected.tm_min);
    EXPECT_EQ(loaded.tm_sec, expected.tm_sec);
}