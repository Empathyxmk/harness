#include <gtest/gtest.h>
#include <fstream>
#include <string>
#include <vector>
#include "../../include/keyword_processor.h"

TEST(FileLoad, LoadFromFile) {
    KeywordProcessor kp;
    std::ifstream file("tests/keywords_format_two.txt");
    std::string keyword;
    while (std::getline(file, keyword)) {
        if (!keyword.empty()) kp.addKeyword(keyword);
    }
    auto extracted = kp.extractKeywords("groovy swift objective-c");
    ASSERT_EQ(extracted.size(), 2); // swift, objective-c
    EXPECT_EQ(extracted[0], "swift");
    EXPECT_EQ(extracted[1], "objective-c");
}