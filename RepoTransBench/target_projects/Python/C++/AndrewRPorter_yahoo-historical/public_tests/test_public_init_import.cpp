#include <gtest/gtest.h>
#include "yahoo_historical_fetcher_stub.h"

TEST(PublicInitImportTest, ImportFetcherPublic) {
    Fetcher f("msft", 1650000000, 1650001000);
    EXPECT_EQ(f.create_url("history").find("msft") != std::string::npos, true);
    EXPECT_NO_THROW({
        auto dummy = f.get_historical();
    });
}