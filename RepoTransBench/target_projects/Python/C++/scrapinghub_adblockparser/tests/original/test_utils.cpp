#include <gtest/gtest.h>
#include "adblockparser.h"
#include <vector>
#include <string>
#include <algorithm>

namespace {
bool is_title_case(const std::string &str) {
    if (str.empty()) return false;
    return std::isupper(str[0]);
}
}

TEST(UtilsTest, SplitDataTitles) {
    std::vector<std::string> xs = {"foo", "Bar", "Spam", "egg"};
    auto result = utils::split_data(xs, is_title_case);
    EXPECT_EQ(result.first, std::vector<std::string>({"Bar", "Spam"}));
    EXPECT_EQ(result.second, std::vector<std::string>({"foo", "egg"}));
}

TEST(UtilsTest, SplitDataAllYes) {
    std::vector<std::string> xs = {"Hello", "World"};
    auto result = utils::split_data(xs, is_title_case);
    EXPECT_EQ(result.first, xs);
    EXPECT_TRUE(result.second.empty());
}

TEST(UtilsTest, SplitDataAllNo) {
    std::vector<std::string> xs = {"foo", "bar"};
    auto result = utils::split_data(xs, is_title_case);
    EXPECT_TRUE(result.first.empty());
    EXPECT_EQ(result.second, xs);
}

TEST(UtilsTest, SplitDataEmpty) {
    std::vector<std::string> xs;
    auto result = utils::split_data(xs, is_title_case);
    EXPECT_TRUE(result.first.empty());
    EXPECT_TRUE(result.second.empty());
}