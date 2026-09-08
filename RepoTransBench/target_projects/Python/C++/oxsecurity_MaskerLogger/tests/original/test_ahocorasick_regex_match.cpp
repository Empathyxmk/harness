#include <gtest/gtest.h>
#include <string>
#include "../../src/ahocorasick_regex_match.h"

using maskerlogger::RegexMatcher;

TEST(TestRegexMatcher, FindMatchesAndMask) {
    RegexMatcher matcher("", 90);
    std::string msg = "password: hunter2";
    auto matches = matcher.find_matches(msg);
    ASSERT_FALSE(matches.empty());
    std::string masked = matcher.mask(msg);
    ASSERT_NE(masked.find("***"), std::string::npos);
}

TEST(TestRegexMatcher, ParseConfigFailure) {
    RegexMatcher matcher("nonexistent_path.toml", 80);
    std::string out = matcher.mask("password: hunter2 super");
    ASSERT_NE(out.find("*"), std::string::npos);
}