#include <gtest/gtest.h>
#include <string>
#include "../../include/keyword_processor.h"

TEST(PublicExtractFuzzy, Fuzzy) {
    KeywordProcessor kp;
    kp.addKeyword("javvs", "java");
    kp.setFuzzyExtract(true);
    kp.setFuzzyDistance(2);
    auto found = kp.extractKeywords("javvs is nice");
    ASSERT_EQ(found.size(), 1);
    EXPECT_EQ(found[0], "java");
}