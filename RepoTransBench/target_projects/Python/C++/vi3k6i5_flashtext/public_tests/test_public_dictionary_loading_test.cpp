#include <gtest/gtest.h>
#include <fstream>
#include <vector>
#include <string>
#include <map>
#include "../../include/keyword_processor.h"

static std::vector<std::string> read_keywords(const std::string& filename) {
    std::vector<std::string> result;
    std::ifstream file(filename);
    std::string line;
    while (std::getline(file, line)) {
        if (!line.empty()) result.push_back(line);
    }
    return result;
}

TEST(PublicDictionaryLoading, CanLoadFromTxtFile) {
    KeywordProcessor kp;
    auto keys = read_keywords("tests/keywords_format_one.txt");
    for (const auto& k : keys) kp.addKeyword(k);
    EXPECT_TRUE(kp.hasKeyword("scala"));
}

TEST(PublicDictionaryLoading, CanAddKeywordMapping) {
    KeywordProcessor kp;
    std::map<std::string, std::string> mapping = {{"go", "golang"}, {"js", "javascript"}};
    for (const auto& kv : mapping) kp.addKeyword(kv.first, kv.second);
    auto found = kp.extractKeywords("I use go and js");
    ASSERT_EQ(found.size(), 2);
    EXPECT_EQ(found[0], "golang");
    EXPECT_EQ(found[1], "javascript");
}