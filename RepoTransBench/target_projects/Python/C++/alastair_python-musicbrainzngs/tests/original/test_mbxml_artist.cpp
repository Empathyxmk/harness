#include <gtest/gtest.h>
#include <string>
#include <vector>
#include <map>
#include <filesystem>
#include "../test_helpers/common_test_utils.h"

// Tests for parsing of artist queries

class GetArtistTest : public ::testing::Test {
protected:
    std::string datadir;
    void SetUp() override {
        // Assuming helpers provide a way to get test file path
        datadir = std::filesystem::path(__FILE__).parent_path().string() + "/data/artist";
    }
};

TEST_F(GetArtistTest, testArtistAliases) {
    auto res = open_and_parse_test_data(datadir, "0e43fe9d-c472-4b62-be9e-55f971a023e1-aliases.xml");
    auto aliases = res["artist"]["alias-list"];
    ASSERT_EQ(aliases.size(), 28u);

    auto a0 = aliases[0];
    EXPECT_EQ(a0["alias"], "Prokofief");
    EXPECT_EQ(a0["sort-name"], "Prokofief");

    auto a17 = aliases[17];
    EXPECT_EQ(a17["alias"], "Sergei Sergeyevich Prokofiev");
    EXPECT_EQ(a17["sort-name"], "Prokofiev, Sergei Sergeyevich");
    EXPECT_EQ(a17["locale"], "en");
    EXPECT_EQ(a17["primary"], "primary");

    res = open_and_parse_test_data(datadir, "2736bad5-6280-4c8f-92c8-27a5e63bbab2-aliases.xml");
    EXPECT_TRUE(res["artist"].find("alias-list") == res["artist"].end());
}

TEST_F(GetArtistTest, testArtistTargets) {
    auto res = open_and_parse_test_data(datadir, "b3785a55-2cf6-497d-b8e3-cfa21a36f997-artist-rels.xml");
    ASSERT_TRUE(res["artist"]["artist-relation-list"][0].find("target-credit") != res["artist"]["artist-relation-list"][0].end());
    EXPECT_EQ(res["artist"]["artist-relation-list"][0]["target-credit"], "TAO");
}