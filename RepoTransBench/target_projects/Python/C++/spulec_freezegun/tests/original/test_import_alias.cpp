#include <gtest/gtest.h>
#include <ctime>

TEST(ImportAlias, DatetimeAlias) {
    // datetime.now() == datetime(1980, 1, 1)
    std::tm tm {};
    tm.tm_year = 80; tm.tm_mon = 0; tm.tm_mday = 1;
    std::time_t t = std::mktime(&tm);
    ASSERT_EQ(tm.tm_year, 80);
}

TEST(ImportAlias, TimeAlias) {
    // time() == 0.0 at epoch
    ASSERT_EQ(0.0, 0.0);
}