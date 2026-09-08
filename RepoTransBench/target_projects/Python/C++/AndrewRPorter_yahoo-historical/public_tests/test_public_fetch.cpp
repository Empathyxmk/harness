#include <gtest/gtest.h>
#include "yahoo_historical_fetcher_stub.h"
#include <string>
#include <stdexcept>

TEST(PublicFetchTest, FetcherCreateUrlPublic) {
    Fetcher f("NFLX", 1500000000, 1500500000);
    std::string url = f.create_url("history");
    EXPECT_NE(url.find("NFLX"), std::string::npos);
    EXPECT_NE(url.find("history"), std::string::npos);
}

TEST(PublicFetchTest, FetcherInvalidIntervalPublic) {
    Fetcher f("NFLX", 1510000000, 1510500000, "8h");
    EXPECT_THROW({
        f.get_historical();
    }, std::exception);
}

TEST(PublicFetchTest, FetcherGetHistoricalDataframePublic) {
    // test that output string is of expected form (CSV), not actual DataFrame
    Fetcher f("AMZN", 1550000000, 1550600000);
    std::string df = f.get_historical();
    EXPECT_NE(df.find("col1"), std::string::npos);
    EXPECT_NE(df.find("col2"), std::string::npos);
}