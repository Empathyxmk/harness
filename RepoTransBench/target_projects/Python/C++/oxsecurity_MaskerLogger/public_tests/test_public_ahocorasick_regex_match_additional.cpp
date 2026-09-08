#include <gtest/gtest.h>
#include <string>
#include <vector>
#include "../src/ahocorasick_regex_match.h"

using maskerlogger::_build_ahocorasick;

TEST(TestAhoCorasickRegexMatchAdditionalPublic, EmptyTrie) {
    auto trie = _build_ahocorasick({});
    auto matches = trie.iter("this string has nothing of interest");
    ASSERT_TRUE(matches.empty());
}

TEST(TestAhoCorasickRegexMatchAdditionalPublic, PartialMatchNotFound) {
    auto trie = _build_ahocorasick({"dog", "cat", "mouse"});
    std::string s = "The quick brown fox.";
    auto matches = trie.iter(s);
    std::vector<std::string> found;
    for (const auto& m : matches) {
        found.push_back(m.word);
    }
    ASSERT_TRUE(found.empty());
}