#include <gtest/gtest.h>
#include <string>
#include <vector>
#include <map>
#include "linkedin2username.h"

// Note: The public test seems to expect GEO_REGIONS to be a vector of maps with keys "countryCode", "name"
// We'll assume both .at("countryCode") and .at("name") exist for these regions.

TEST(PublicGeoRegions, GeoRegionsGB) {
    std::vector<std::map<std::string, std::string>> us_region;
    for (const auto& region : GEO_REGIONS_LIST) {
        if (region.at("countryCode") == "GB") {
            us_region.push_back(region);
        }
    }
    ASSERT_FALSE(us_region.empty()) << "Should find regions for GB";
    for (const auto& region : us_region) {
        EXPECT_TRUE(region.find("countryCode") != region.end());
        EXPECT_TRUE(region.find("name") != region.end());
        EXPECT_EQ(region.at("countryCode"), "GB");
    }
}

TEST(PublicGeoRegions, GeoRegionsAllHaveStr) {
    for (const auto& region : GEO_REGIONS_LIST) {
        EXPECT_TRUE(typeid(region.at("name")) == typeid(std::string));
    }
}