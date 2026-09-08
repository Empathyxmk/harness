#include <gtest/gtest.h>
#include "adblockparser.h"

namespace {
bool is_public_title_case(const std::string &str) {
    if (str.empty()) return false;
    return std::isupper(str[0]);
}
}

TEST(PublicUtilsTest, PublicSplitDataTitles) {
    std::vector<std::string> xs = {"Joe", "amy", "Mike", "susan"};
    auto result = utils::split_data(xs, is_public_title_case);
    EXPECT_EQ(result.first, std::vector<std::string>({"Joe", "Mike"}));
    EXPECT_EQ(result.second, std::vector<std::string>({"amy", "susan"}));
}

TEST(PublicUtilsTest, PublicSplitDataAllYes) {
    std::vector<std::string> xs = {"Alpha", "Beta"};
    auto result = utils::split_data(xs, is_public_title_case);
    EXPECT_EQ(result.first, xs);
    EXPECT_TRUE(result.second.empty());
}

TEST(PublicUtilsTest, PublicSplitDataAllNo) {
    std::vector<std::string> xs = {"gamma", "delta"};
    auto result = utils::split_data(xs, is_public_title_case);
    EXPECT_TRUE(result.first.empty());
    EXPECT_EQ(result.second, xs);
}

TEST(PublicUtilsTest, PublicSplitDataEmpty) {
    std::vector<std::string> xs;
    auto result = utils::split_data(xs, is_public_title_case);
    EXPECT_TRUE(result.first.empty());
    EXPECT_TRUE(result.second.empty());
}