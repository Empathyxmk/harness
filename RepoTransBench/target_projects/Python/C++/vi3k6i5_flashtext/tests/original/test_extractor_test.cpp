#include <gtest/gtest.h>
#include <string>
#include <vector>
#include "../../include/keyword_processor.h"

TEST(Extractor, BasicExtraction) {
    KeywordProcessor kp;
    kp.addKeyword("java");
    kp.addKeyword("python");
    std::vector<std::string> result = kp.extractKeywords("I code in java and python.");
    ASSERT_EQ(result.size(), 2);
    EXPECT_EQ(result[0], "java");
    EXPECT_EQ(result[1], "python");
}

TEST(Extractor, CaseInsensitivity) {
    KeywordProcessor kp;
    kp.addKeyword("JavaScript");
    kp.addKeyword("HTML");
    std::vector<std::string> result = kp.extractKeywords("JAVASCRIPT and Html are web technologies.");
    ASSERT_EQ(result.size(), 2);
    EXPECT_EQ(result[0], "JavaScript");
    EXPECT_EQ(result[1], "HTML");
}

TEST(Extractor, ReplacementExtraction) {
    KeywordProcessor kp;
    kp.addKeyword("java", "Java");
    kp.addKeyword("python", "Python");
    std::vector<std::string> result = kp.extractKeywords("java python scripting");
    ASSERT_EQ(result.size(), 2);
    EXPECT_EQ(result[0], "Java");
    EXPECT_EQ(result[1], "Python");
}