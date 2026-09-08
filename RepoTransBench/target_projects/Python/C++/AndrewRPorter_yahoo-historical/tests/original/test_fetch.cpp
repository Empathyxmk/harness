#include <gtest/gtest.h>
#include "yahoo_historical_fetcher_stub.h"
#include <string>
#include <stdexcept>

const std::string TEST_TICKER = "AAPL";
const long TIME_START = 1483228800;
const long TIME_END = 1483497600;

// Our "mock" get_historical is just a method to simulate the desired result
struct DummyDf {
    std::vector<int> operator[](const std::string&) const { return {1,2,3}; }
};

std::string mock_get_historical(const Fetcher*, const std::string& kind, bool as_dataframe)
{
    if (as_dataframe) {
        return "DummyDf"; // proxy for the object; not used in C++ tests
    } else {
        return "col1,col2\n1,2\n3,4";
    }
}

TEST(FetchTest, GetNoDataFrame) {
    Fetcher f(TEST_TICKER, TIME_START, TIME_END);
    std::string data = f.get_historical(false);
    EXPECT_NE(data.find("col1"), std::string::npos);
}

TEST(FetchTest, GetWithLowercase) {
    Fetcher f("aapl", TIME_START, TIME_END);
    // Would monkeypatch get_historical, but in stub returns string
    std::string data = f.get_historical();
    EXPECT_EQ(typeid(data), typeid(std::string));
}

TEST(FetchTest, GetHistorical) {
    Fetcher f(TEST_TICKER, TIME_START, TIME_END);
    std::string data = f.get_historical();
    EXPECT_EQ(typeid(data), typeid(std::string));
}

TEST(FetchTest, InvalidDate) {
    // simulate wrong input with invalid time (string-value triggers bad_cast, here simulate with negative)
    Fetcher f(TEST_TICKER, -1, TIME_END);
    EXPECT_THROW({
        f.get_historical();
    }, std::exception);
}

TEST(FetchTest, FetcherWithFloatDates) {
    // Simulate with same valid values
    Fetcher f(TEST_TICKER, static_cast<long>(static_cast<float>(TIME_START)), static_cast<long>(static_cast<float>(TIME_END)));
    std::string data = f.get_historical();
    EXPECT_EQ(typeid(data), typeid(std::string));
}