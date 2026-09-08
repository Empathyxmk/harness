#include <gtest/gtest.h>
#include "yahoo_historical_fetcher_stub.h"

TEST(InitImportTest, ImportFetcher) {
    Fetcher f("aapl", 1600000000, 1600001000);
    EXPECT_EQ(f.create_url("history").find("aapl") != std::string::npos, true);
    EXPECT_NO_THROW({
        auto dummy = f.get_historical();
    });
}