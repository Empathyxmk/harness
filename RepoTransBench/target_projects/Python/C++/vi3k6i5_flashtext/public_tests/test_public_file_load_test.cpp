#include <gtest/gtest.h>
#include <string>
#include <vector>
#include <fstream>
#include "../../include/keyword_processor.h"

TEST(PublicFileLoad, ReadingFile) {
    KeywordProcessor kp;
    std::ifstream file("tests/keywords_format_two.txt");
    std::string word;
    while (std::getline(file, word)) {
        if (!word.empty()) kp.addKeyword(word);
    }
    auto found = kp.extractKeywords("objective-c swift");
    ASSERT_EQ(found.size(), 2);
    EXPECT_EQ(found[0], "objective-c");
    EXPECT_EQ(found[1], "swift");
}