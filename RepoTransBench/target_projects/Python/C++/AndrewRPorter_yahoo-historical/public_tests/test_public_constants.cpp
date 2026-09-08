#include <gtest/gtest.h>
#include "yahoo_historical_constants_stub.h"
#include <string>

TEST(PublicConstantsTest, ConstantsFieldsPublic) {
    using namespace Constants;
    EXPECT_EQ(API_URL.empty(), false);
    EXPECT_EQ(DATE_INTERVALS.count("1d") > 0, true);
    EXPECT_EQ(ONE_DAY_INTERVAL, "1d");
}

TEST(PublicConstantsTest, ApiUrlFormatPublic) {
    using namespace Constants;
    char buf[300];
    snprintf(buf, sizeof(buf), API_URL.c_str(), "TSLA", 1610000000L, 1610020000L, "1d", "history");
    std::string url(buf);
    EXPECT_NE(url.find("TSLA"), std::string::npos);
    EXPECT_NE(url.find("16100"), std::string::npos);
    EXPECT_NE(url.find("1d"), std::string::npos);
    EXPECT_GT(url.find("history"), 0u);
}