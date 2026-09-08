#include <gtest/gtest.h>
#include <string>
#include <map>
#include "linkedin2username.h"

TEST(GeoRegions, USRegionKey) {
    // Should match the value for "us"
    ASSERT_EQ(GEO_REGIONS.at("us"), "103644278");
}

TEST(GeoRegions, AllHaveStr) {
    for (const auto& region : GEO_REGIONS) {
        EXPECT_TRUE(typeid(region.first) == typeid(std::string));
        EXPECT_TRUE(typeid(region.second) == typeid(std::string));
        for (char c : region.second) {
            EXPECT_TRUE(isdigit(c));
        }
    }
}