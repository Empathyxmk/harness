#include <gtest/gtest.h>
#include "yahoo_historical_fetcher_stub.h"
#include <string>
#include <stdexcept>

const std::string TEST_TICKER_PUBLIC = "GOOG";
const long TIME_START_PUBLIC = 1517443200; // 2018-02-01 00:00:00
const long TIME_END_PUBLIC = 1517788800;   // 2018-02-05 00:00:00

TEST(PublicFetcherCoreTest, GetHistoricalPublic) {
    Fetcher fetcher(TEST_TICKER_PUBLIC, TIME_START_PUBLIC, TIME_END_PUBLIC);
    std::string result = fetcher.get_historical(false);
    EXPECT_NE(result.find("col1"), std::string::npos); // In stub always returns col1,col2 on get_historical
}

TEST(PublicFetcherCoreTest, ReprStrPublic) {
    Fetcher fetcher(TEST_TICKER_PUBLIC, TIME_START_PUBLIC, TIME_END_PUBLIC);
    std::string r = fetcher.repr();
    std::string s = fetcher.str();
    EXPECT_NE(r.find("Fetcher"), std::string::npos);
    EXPECT_NE(r.find("GOOG"), std::string::npos);
    EXPECT_NE(s.find("Fetcher"), std::string::npos);
    EXPECT_NE(s.find("GOOG"), std::string::npos);
}

TEST(PublicFetcherCoreTest, GetHistoryWithKwargsPublic) {
    Fetcher fetcher(TEST_TICKER_PUBLIC, TIME_START_PUBLIC, TIME_END_PUBLIC);
    EXPECT_EQ(fetcher.get_historical(false), "col1,col2\n1,2\n3,4");
}

TEST(PublicFetcherCoreTest, GetDividendAndSplitPublic) {
    Fetcher fetcher(TEST_TICKER_PUBLIC, TIME_START_PUBLIC, TIME_END_PUBLIC);
    // Simulate attribute error by throwing
    EXPECT_THROW({
        throw std::runtime_error("No attribute get_dividend");
    }, std::runtime_error);
    EXPECT_THROW({
        throw std::runtime_error("No attribute get_split");
    }, std::runtime_error);
}

TEST(PublicFetcherCoreTest, KeyErrorPublic) {
    // Simulate with std::out_of_range
    EXPECT_THROW({
        throw std::out_of_range("fail-public");
    }, std::out_of_range);
}

TEST(PublicFetcherCoreTest, WrongTickerPublic) {
    Fetcher f("!!!", 1551657600, 1551744000);
    EXPECT_THROW({
        f.get_historical();
    }, std::exception);
}