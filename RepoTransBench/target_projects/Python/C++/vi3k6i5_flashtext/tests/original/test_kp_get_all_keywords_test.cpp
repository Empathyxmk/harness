#include <gtest/gtest.h>
#include <vector>
#include <string>
#include "../../include/keyword_processor.h"

TEST(KpGetAllKeywords, ReturnsAllKeywords) {
    KeywordProcessor kp;
    kp.addKeyword("java");
    kp.addKeyword("python");
    std::vector<std::string> all = kp.getAllKeywords();
    ASSERT_EQ(all.size(), 2);
    EXPECT_NE(std::find(all.begin(), all.end(), "java"), all.end());
    EXPECT_NE(std::find(all.begin(), all.end(), "python"), all.end());
}