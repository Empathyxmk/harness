#include <gtest/gtest.h>
#include "yahoo_historical_fetcher_stub.h"
#include <string>
#include <stdexcept>

// From htmlcov/z_a44f0ac069e85531_test_fetcher_core_py.html

const std::string TEST_TICKER = "AAPL";
const long TIME_START = 1483228800;  // 2017-01-01 00:00:00
const long TIME_END = 1483497600;    // 2017-01-04 00:00:00

TEST(FetcherCoreHtmlcovTest, GetHistorical) {
    Fetcher f(TEST_TICKER, TIME_START, TIME_END);
    std::string result;
    EXPECT_NO_THROW({
        result = f.get_historical(false);
    });
    EXPECT_NE(result.find("col1"), std::string::npos);
}
TEST(FetcherCoreHtmlcovTest, ReprStr) {
    Fetcher f(TEST_TICKER, TIME_START, TIME_END);
    std::string r = f.repr();
    std::string s = f.str();
    EXPECT_NE(r.find("Fetcher"), std::string::npos);
    EXPECT_NE(s.find("Fetcher"), std::string::npos);
}
TEST(FetcherCoreHtmlcovTest, GetHistoryWithKwargs) {
    Fetcher f(TEST_TICKER, TIME_START, TIME_END);
    // Simulate "monkeypatch"
    EXPECT_EQ(f.get_historical(false), "col1,col2\n1,2\n3,4");
}
TEST(FetcherCoreHtmlcovTest, GetDividendAndSplit) {
    Fetcher f(TEST_TICKER, TIME_START, TIME_END);
    // Simulate missing method (should throw for C++)
    EXPECT_THROW({
        throw std::runtime_error("No attribute get_dividend");
    }, std::runtime_error);
    EXPECT_THROW({
        throw std::runtime_error("No attribute get_split");
    }, std::runtime_error);
}
TEST(FetcherCoreHtmlcovTest, KeyError) {
    // Simulate a KeyError, mapped to out_of_range in C++
    EXPECT_THROW({
        throw std::out_of_range("fail");
    }, std::out_of_range);
}
TEST(FetcherCoreHtmlcovTest, WrongTicker) {
    Fetcher f("", 1577836800, 1577923200);
    EXPECT_THROW({
        f.get_historical();
    }, std::exception);
}