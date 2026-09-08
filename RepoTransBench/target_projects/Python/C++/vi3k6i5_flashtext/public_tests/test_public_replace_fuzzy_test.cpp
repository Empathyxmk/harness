#include <gtest/gtest.h>
#include <string>
#include "../../include/keyword_processor.h"

TEST(PublicReplaceFuzzy, Replace) {
    KeywordProcessor kp;
    kp.addKeyword("javascrpt", "javascript");
    kp.setFuzzyExtract(true);
    kp.setFuzzyDistance(1);
    auto replaced = kp.replaceKeywords("javascrpt rocks");
    EXPECT_EQ(replaced, "javascript rocks");
}