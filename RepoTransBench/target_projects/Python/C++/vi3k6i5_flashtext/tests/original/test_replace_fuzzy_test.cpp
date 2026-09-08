#include <gtest/gtest.h>
#include <string>
#include <vector>
#include "../../include/keyword_processor.h"

TEST(ReplaceFuzzy, FuzzyReplacement) {
    KeywordProcessor kp;
    kp.addKeyword("javscript", "javascript");
    kp.setFuzzyExtract(true);
    std::string replaced = kp.replaceKeywords("I love javscript!");
    EXPECT_EQ(replaced, "I love javascript!");
}