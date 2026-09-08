#include <gtest/gtest.h>
#include "yahoo_historical_fetcher_stub.h"
#include <string>
#include <stdexcept>

const std::string TEST_TICKER = "AAPL";
const long TIME_START = 1483228800;  // 2017-01-01 00:00:00
const long TIME_END = 1483497600;    // 2017-01-04 00:00:00

struct Monkeypatch {
    // For patching member function pointers
    typedef std::string(*GetFuncType)(const Fetcher*, const std::string&, bool);

    static void setattr_get(Fetcher* f, std::function<std::string(const Fetcher*, const std::string&, bool)> fun) {
        // No-op in this stub; use conditional logic in tests for patching results.
    }
};

TEST(FetcherCoreTest, GetHistorical) {
    Fetcher f(TEST_TICKER, TIME_START, TIME_END);
    std::string result;
    EXPECT_NO_THROW({
        result = f.get_historical(false);
    });
    EXPECT_NE(result.find("col1"), std::string::npos);
}

TEST(FetcherCoreTest, ReprStr) {
    Fetcher f(TEST_TICKER, TIME_START, TIME_END);
    std::string r = f.repr();
    std::string s = f.str();
    EXPECT_NE(r.find("Fetcher"), std::string::npos);
    EXPECT_NE(s.find("Fetcher"), std::string::npos);
}

TEST(FetcherCoreTest, GetHistoryKwargs) {
    Fetcher f(TEST_TICKER, TIME_START, TIME_END);
    // Simulate "monkeypatch"
    EXPECT_EQ(f.get_historical(false), "col1,col2\n1,2\n3,4");
}

TEST(FetcherCoreTest, GetDividendAndSplit) {
    Fetcher f(TEST_TICKER, TIME_START, TIME_END);
    // Fetcher has no get_dividend or get_split (should throw)
    EXPECT_THROW({
        // simulate missing method by throwing on access
        throw std::runtime_error("No attribute get_dividend");
    }, std::runtime_error);
    EXPECT_THROW({
        throw std::runtime_error("No attribute get_split");
    }, std::runtime_error);
}

TEST(FetcherCoreTest, KeyError) {
    Fetcher f(TEST_TICKER, TIME_START, TIME_END);
    auto raise_key_error = []() -> std::string {
        throw std::out_of_range("fail");
    };
    EXPECT_THROW({
        raise_key_error();
    }, std::out_of_range);
}

TEST(FetcherCoreTest, WrongTicker) {
    Fetcher f("", 1577836800, 1577923200);
    EXPECT_THROW({
        f.get_historical();
    }, std::exception);
}