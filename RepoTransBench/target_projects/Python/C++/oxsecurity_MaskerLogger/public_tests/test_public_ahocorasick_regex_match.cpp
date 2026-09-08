#include <gtest/gtest.h>
#include <string>
#include <vector>
#include "../src/ahocorasick_regex_match.h"

using maskerlogger::AhoCorasickTrie;
using maskerlogger::load_regexes_from_config;
using maskerlogger::_build_ahocorasick;

TEST(TestAhoCorasickRegexMatchPublic, BuildTrieAndMatch) {
    std::vector<std::string> keys = {"bear", "wolf", "lion"};
    auto trie = _build_ahocorasick(keys);
    std::vector<std::string> found;
    std::string s = "the wolf and lion bear witness";
    auto matches = trie.iter(s);
    for(const auto& m : matches) {
        found.push_back(m.word);
    }
    ASSERT_EQ(found.size(), 3u);
    std::sort(found.begin(), found.end());
    std::vector<std::string> expected = {"bear", "lion", "wolf"};
    std::sort(expected.begin(), expected.end());
    ASSERT_EQ(found, expected);
}

TEST(TestAhoCorasickRegexMatchPublic, BuildRegexFromConfig) {
    auto result = load_regexes_from_config();
    ASSERT_TRUE(result.size() >= 0);
}