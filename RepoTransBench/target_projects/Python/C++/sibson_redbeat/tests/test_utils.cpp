#include <gtest/gtest.h>
#include <chrono>
#include <ctime>

// Assume from_timestamp and to_timestamp both round to the nearest second (no microseconds)
std::time_t to_timestamp(const std::tm& t) {
    return timegm(const_cast<std::tm*>(&t));
}
std::tm from_timestamp(std::time_t ts) {
    std::tm res{};
    gmtime_r(&ts, &res);
    return res;
}

class UtilsTest : public ::testing::Test {
};

TEST_F(UtilsTest, Roundtrip) {
    std::tm now;
    time_t t = time(0);
    gmtime_r(&t, &now);

    std::time_t ts = to_timestamp(now);
    std::tm roundtripped = from_timestamp(ts);

    now.tm_sec = roundtripped.tm_sec; // Ignore milliseconds
    EXPECT_EQ(now.tm_year, roundtripped.tm_year);
    EXPECT_EQ(now.tm_mon, roundtripped.tm_mon);
    EXPECT_EQ(now.tm_mday, roundtripped.tm_mday);
    EXPECT_EQ(now.tm_hour, roundtripped.tm_hour);
    EXPECT_EQ(now.tm_min, roundtripped.tm_min);
}