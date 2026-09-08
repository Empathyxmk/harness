#include <gtest/gtest.h>
#include <fstream>
#include <string>
#include <vector>
#include <map>
#include "../../include/keyword_processor.h"

// Utility to load keywords from file (one per line)
static std::vector<std::string> load_keywords(const std::string& filename) {
    std::ifstream file(filename);
    std::vector<std::string> keywords;
    std::string line;
    while (std::getline(file, line)) {
        if (!line.empty()) {
            keywords.push_back(line);
        }
    }
    return keywords;
}

TEST(DictionaryLoading, LoadWordsFromTextFileFormatOne) {
    KeywordProcessor kp;
    auto keywords = load_keywords("tests/keywords_format_one.txt");
    for (const auto& k : keywords) {
        kp.addKeyword(k);
    }
    EXPECT_TRUE(kp.hasKeyword("java"));
    EXPECT_TRUE(kp.hasKeyword("scala"));
    EXPECT_FALSE(kp.hasKeyword("perl"));
}

TEST(DictionaryLoading, LoadMapFromJsonFormat) {
    KeywordProcessor kp;
    std::map<std::string, std::string> keyword_map = {
        {"C++", "cplusplus"},
        {"java", "java"}
    };
    for (const auto& kv : keyword_map) {
        kp.addKeyword(kv.first, kv.second);
    }
    EXPECT_EQ(kp.extractKeywords("I code in C++ and java")[0], "cplusplus");
    EXPECT_EQ(kp.extractKeywords("I use java daily")[0], "java");
}

TEST(DictionaryLoading, AddKeywordsFromList) {
    KeywordProcessor kp;
    std::vector<std::string> word_list = {"perl", "ruby", "swift"};
    for (const auto& word : word_list) kp.addKeyword(word);
    auto found = kp.extractKeywords("I like perl and ruby.");
    ASSERT_EQ(found.size(), 2);
    EXPECT_EQ(found[0], "perl");
    EXPECT_EQ(found[1], "ruby");
}