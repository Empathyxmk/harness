#include <gtest/gtest.h>
#include "yahoo_historical_fetcher_stub.h"
// From htmlcov/d_a44f0ac069e85531_test_init_import_py.html

TEST(InitImportHtmlcovTest, ImportFetcherHtmlcov) {
    Fetcher f("aapl", 1600000000, 1600001000);
    EXPECT_EQ(f.create_url("history").find("aapl") != std::string::npos, true);
    EXPECT_NO_THROW({
        auto dummy = f.get_historical();
    });
}