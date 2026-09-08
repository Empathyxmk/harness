#include <gtest/gtest.h>
#include <string>
#include <vector>
#include <map>
#include <filesystem>
#include "../test_helpers/common_test_utils.h"

// Tests for parsing of label queries

class GetLabelTest : public ::testing::Test {
protected:
    std::string datadir;
    void SetUp() override {
        // Assuming helpers provide a way to get test file path
        datadir = std::filesystem::path(__FILE__).parent_path().string() + "/data/label";
    }
};

TEST_F(GetLabelTest, testLabelAliases) {
    auto res = open_and_parse_test_data(datadir, "022fe361-596c-43a0-8e22-bad712bb9548-aliases.xml");
    auto aliases = res["label"]["alias-list"];
    ASSERT_EQ(aliases.size(), 4u);

    auto a0 = aliases[0];
    EXPECT_EQ(a0["alias"], "EMI");
    EXPECT_EQ(a0["sort-name"], "EMI");

    auto a1 = aliases[1];
    EXPECT_EQ(a1["alias"], "EMI Records (UK)");
    EXPECT_EQ(a1["sort-name"], "EMI Records (UK)");

    res = open_and_parse_test_data(datadir, "e72fabf2-74a3-4444-a9a5-316296cbfc8d-aliases.xml");
    aliases = res["label"]["alias-list"];
    ASSERT_EQ(aliases.size(), 1u);

    a0 = aliases[0];
    EXPECT_EQ(a0["alias"], "Ki/oon Records Inc.");
    EXPECT_EQ(a0["sort-name"], "Ki/oon Records Inc.");
    EXPECT_EQ(a0["begin-date"], "2001-10");
    EXPECT_EQ(a0["end-date"], "2012-04");
}