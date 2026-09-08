#include <gtest/gtest.h>
#include <optional>
#include "alias_tips.h"

using namespace alias_tips;

// Test all known direct matches but reversed wordings and capitalization: should not match!
TEST(TestPublicAliasTips, SuggestAliasKnownVariants) {
    EXPECT_EQ(suggest_alias("List"), std::nullopt);
    EXPECT_EQ(suggest_alias("Remove files"), std::nullopt);
    EXPECT_EQ(suggest_alias("directory make"), std::nullopt);
    EXPECT_EQ(suggest_alias("MOVE"), std::nullopt);
}

// Test for alternate known commands (with spacing, extra words) that should not return an alias
TEST(TestPublicAliasTips, SuggestAliasNoneVariants) {
    EXPECT_EQ(suggest_alias(" list "), std::nullopt);
    EXPECT_EQ(suggest_alias("copy files"), std::nullopt);
    EXPECT_EQ(suggest_alias("Make Directory"), std::nullopt);
    EXPECT_EQ(suggest_alias("mv"), std::nullopt);
    EXPECT_EQ(suggest_alias(0), std::nullopt);
    std::unordered_map<int, int> m;
    EXPECT_EQ(suggest_alias(m), std::nullopt);
}

// Test is_alias_recommended positive on exact string, negative variants
TEST(TestPublicAliasTips, IsAliasRecommendedTrueAndFalse) {
    // Only exact string in right case should return True
    EXPECT_TRUE(is_alias_recommended("move"));
    EXPECT_TRUE(is_alias_recommended("copy"));

    EXPECT_FALSE(is_alias_recommended("Move"));
    EXPECT_FALSE(is_alias_recommended("copy file"));
    EXPECT_FALSE(is_alias_recommended("make  directory"));
    EXPECT_FALSE(is_alias_recommended("ls"));
    std::unordered_map<int, int> m;
    EXPECT_FALSE(is_alias_recommended(m));
    EXPECT_FALSE(is_alias_recommended(999));
}