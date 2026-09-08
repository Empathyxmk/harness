#include <gtest/gtest.h>
#include <string>
#include <vector>
#include <algorithm>
#include "fuzzywuzzy/fuzz.h"

// Helper for generating representative string test data.
std::vector<std::pair<std::string, std::string>> getTestStringPairs() {
    return {
        {"", ""},
        {"a", "a"},
        {"kitten", "sitting"},
        {"test", "taste"},
        {"", "nonempty"},
        {"nonempty", ""},
        {"abc", "cba"},
        {"levenshtein", "levenshtein"},
        {"hello", "hello world"},
        {"fuzzy", "wuzzy"},
    };
}

// Property test: ratio is symmetric (ratio(a, b) == ratio(b, a))
TEST(FuzzyWuzzyHypothesis, RatioSymmetry) {
    auto test_cases = getTestStringPairs();
    for (const auto& p : test_cases) {
        int score_ab = fuzzywuzzy::fuzz::ratio(p.first, p.second);
        int score_ba = fuzzywuzzy::fuzz::ratio(p.second, p.first);
        EXPECT_EQ(score_ab, score_ba) << "Symmetry failed for: " << p.first << " and " << p.second;
    }
}

// Property test: ratio("x", "x") == 100 for any x
TEST(FuzzyWuzzyHypothesis, RatioNormalizationOnIdentity) {
    std::vector<std::string> test_cases = {
        "", "a", "kitten", "test", "fuzzy", "levenshtein", "x", "verylongstringwithnospaces"
    };
    for (const auto& s : test_cases) {
        EXPECT_EQ(fuzzywuzzy::fuzz::ratio(s, s), 100) << "Failed normalization for: " << s;
    }
}

// Property test: ratio between empty string and anything else is 0 (unless both empty)
TEST(FuzzyWuzzyHypothesis, RatioEmptyString) {
    std::string empty = "";
    std::vector<std::string> test_cases = {
        "", "a", "abc", "fuzzy", "   ", "0", "something", "wuzzy"
    };
    for (const auto& s : test_cases) {
        if (s.empty()) {
            EXPECT_EQ(fuzzywuzzy::fuzz::ratio(empty, s), 100);
        } else {
            EXPECT_EQ(fuzzywuzzy::fuzz::ratio(empty, s), 0);
            EXPECT_EQ(fuzzywuzzy::fuzz::ratio(s, empty), 0);
        }
    }
}

// Property test: ratio accepts all valid std::string input and does not throw.
TEST(FuzzyWuzzyHypothesis, RatioAcceptsAllStringInput) {
    auto test_cases = getTestStringPairs();
    for (const auto& p : test_cases) {
        EXPECT_NO_THROW({
            (void)fuzzywuzzy::fuzz::ratio(p.first, p.second);
        }) << "Exception thrown for inputs: " << p.first << ", " << p.second;
    }
}

// For the other fuzz algorithms (like partial_ratio, token_sort_ratio), we test only presence, symmetry, and no throw.
TEST(FuzzyWuzzyHypothesis, PartialRatioSymmetryAndNoThrow) {
    auto test_cases = getTestStringPairs();
    for (const auto& p : test_cases) {
        int ab = fuzzywuzzy::fuzz::partial_ratio(p.first, p.second);
        int ba = fuzzywuzzy::fuzz::partial_ratio(p.second, p.first);
        EXPECT_EQ(ab, ba) << "Partial ratio symmetry failed for: " << p.first << ", " << p.second;
        EXPECT_NO_THROW({
            (void)fuzzywuzzy::fuzz::partial_ratio(p.first, p.second);
        });
    }
}

TEST(FuzzyWuzzyHypothesis, TokenSortRatioPresenceSymmetry) {
    auto test_cases = getTestStringPairs();
    for (const auto& p : test_cases) {
        int ab = fuzzywuzzy::fuzz::token_sort_ratio(p.first, p.second);
        int ba = fuzzywuzzy::fuzz::token_sort_ratio(p.second, p.first);
        EXPECT_EQ(ab, ba) << "token_sort_ratio symmetry failed for: " << p.first << ", " << p.second;
        EXPECT_NO_THROW({
            (void)fuzzywuzzy::fuzz::token_sort_ratio(p.first, p.second);
        });
    }
}