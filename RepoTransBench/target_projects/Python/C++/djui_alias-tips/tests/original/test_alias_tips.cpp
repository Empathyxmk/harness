#include <gtest/gtest.h>
#include <optional>
#include "alias_tips.h"

using namespace alias_tips;

TEST(TestAliasTips, SuggestAliasKnown) {
    EXPECT_EQ(suggest_alias("list"), std::optional<std::string>("ls"));
    EXPECT_EQ(suggest_alias("remove"), std::optional<std::string>("rm"));
    EXPECT_EQ(suggest_alias("copy"), std::optional<std::string>("cp"));
    EXPECT_EQ(suggest_alias("move"), std::optional<std::string>("mv"));
    EXPECT_EQ(suggest_alias("make directory"), std::optional<std::string>("mkdir"));
}

TEST(TestAliasTips, SuggestAliasNone) {
    EXPECT_EQ(suggest_alias("unknown"), std::nullopt);
    EXPECT_EQ(suggest_alias(""), std::nullopt);

    // None (nullptr input): C++ version is not possible as overload, simulate via explicit null.
    // We will test with std::nullptr_t, which hits the template<> version.
    EXPECT_EQ(suggest_alias(nullptr), std::nullopt);

    EXPECT_EQ(suggest_alias(123), std::nullopt);
    std::vector<int> vec;
    EXPECT_EQ(suggest_alias(vec), std::nullopt);
}

TEST(TestAliasTips, IsAliasRecommendedTrue) {
    EXPECT_TRUE(is_alias_recommended("list"));
    EXPECT_TRUE(is_alias_recommended("remove"));
    EXPECT_TRUE(is_alias_recommended("copy"));
    EXPECT_TRUE(is_alias_recommended("move"));
    EXPECT_TRUE(is_alias_recommended("make directory"));
}

TEST(TestAliasTips, IsAliasRecommendedFalse) {
    EXPECT_FALSE(is_alias_recommended("something else"));
    EXPECT_FALSE(is_alias_recommended(""));
    EXPECT_FALSE(is_alias_recommended(nullptr));
    EXPECT_FALSE(is_alias_recommended(123));
    std::vector<int> vec;
    EXPECT_FALSE(is_alias_recommended(vec));
}