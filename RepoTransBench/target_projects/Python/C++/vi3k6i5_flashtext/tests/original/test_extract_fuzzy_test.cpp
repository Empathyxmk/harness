#include <gtest/gtest.h>
#include <string>
#include <vector>
#include "../../include/keyword_processor.h"

TEST(ExtractFuzzy, HandlesBasicFuzzyMatch) {
    KeywordProcessor kp;
    kp.addKeyword("pythn", "python"); // typo
    kp.addKeyword("jav", "java");     // prefix
    kp.setFuzzyExtract(true);

    std::string text = "I know pythn and jav best";
    auto found = kp.extractKeywords(text);
    ASSERT_EQ(found.size(), 2);
    EXPECT_EQ(found[0], "python");
    EXPECT_EQ(found[1], "java");
}

TEST(ExtractFuzzy, FuzzyMatchWithDistanceThreshold) {
    KeywordProcessor kp;
    kp.addKeyword("Javascript", "javascript");
    kp.setFuzzyExtract(true);
    kp.setFuzzyDistance(2);

    std::string text = "I like Javascriot";
    auto found = kp.extractKeywords(text);
    ASSERT_EQ(found.size(), 1);
    EXPECT_EQ(found[0], "javascript");
}