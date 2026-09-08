#include <gtest/gtest.h>
#include <string>
#include "../../include/keyword_processor.h"

TEST(Replacer, ReplacesMultipleKeywords) {
    KeywordProcessor kp;
    kp.addKeyword("java", "JAVA");
    kp.addKeyword("python", "PYTHON");
    std::string s = kp.replaceKeywords("java python code");
    EXPECT_EQ(s, "JAVA PYTHON code");
}

TEST(Replacer, NoReplaceIfNotFound) {
    KeywordProcessor kp;
    kp.addKeyword("java", "JAVA");
    std::string s = kp.replaceKeywords("no python here");
    EXPECT_EQ(s, "no python here");
}