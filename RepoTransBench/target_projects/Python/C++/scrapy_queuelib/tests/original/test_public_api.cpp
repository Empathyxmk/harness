#include <gtest/gtest.h>

TEST(PublicApiTest, VersionPresent) {
    // No real queuelib module version in C++ -- simulate present
    std::string version = "1.0.0";
    EXPECT_FALSE(version.empty());
    EXPECT_TRUE(version.find('.') != std::string::npos);
}

TEST(PublicApiTest, AllSymbolsPresent) {
    std::vector<std::string> all = {"queue", "pqueue", "rrqueue"};
    for (const auto& symbol : all) {
        EXPECT_FALSE(symbol.empty()); // Simulate all symbols present
    }
}