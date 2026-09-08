#include <gtest/gtest.h>
#include <string>
#include <vector>
#include <algorithm>
#include "fuzzywuzzy/fuzz.h"

// This public test mirrors the Python hypothesis-based public tests
// It checks key public properties of the fuzz::ratio function as would be permitted in a public testing scenario

// Provide a small, diverse list of test pairs to ensure cross-platform consistency
std::vector<std::pair<std::string, std::string>> getPublicTestStringPairs() {
    return {
        {"", ""},
        {"abc", "abc"},
        {"abc", "cba"},
        {"hello world", "hello"},
        {"the quick brown fox", "the quick brown fox"},
        {"", "test"},
        {"test", ""},
        {"fuzzy", "wuzzy"},
        {"Python", "python"},
        {" ", " "},
    };
}

// Public property: ratio is symmetric
TEST(PublicFuzzyWuzzyHypothesis, RatioSymmetry) {
    auto pairs = getPublicTestStringPairs();
    for (const auto &p : pairs) {
        int score1 = fuzzywuzzy::fuzz::ratio(p.first, p.second);
        int score2 = fuzzywuzzy::fuzz::ratio(p.second, p.first);
        EXPECT_EQ(score1, score2) << "Ratio not symmetric for: " << p.first << " vs " << p.second;
    }
}

// Public property: ratio(x, x) == 100 for any x
TEST(PublicFuzzyWuzzyHypothesis, RatioSelfIs100) {
    auto pairs = getPublicTestStringPairs();
    for (const auto &p : pairs) {
        EXPECT_EQ(fuzzywuzzy::fuzz::ratio(p.first, p.first), 100) 
            << "Ratio with itself failed for: " << p.first;
        EXPECT_EQ(fuzzywuzzy::fuzz::ratio(p.second, p.second), 100) 
            << "Ratio with itself failed for: " << p.second;
    }
}

// Public property: ratio between empty string and non-empty is 0; ratio("", "") == 100
TEST(PublicFuzzyWuzzyHypothesis, RatioHandlesEmptyString) {
    auto pairs = getPublicTestStringPairs();
    for (const auto &p : pairs) {
        if (p.first.empty() && p.second.empty()) {
            EXPECT_EQ(fuzzywuzzy::fuzz::ratio(p.first, p.second), 100);
        } else if (p.first.empty() || p.second.empty()) {
            EXPECT_EQ(fuzzywuzzy::fuzz::ratio(p.first, p.second), 0);
        }
    }
}