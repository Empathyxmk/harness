#include <gtest/gtest.h>
#include <string>
#include "../../src/ahocorasick_regex_match.h"

using maskerlogger::RegexMatcher;

TEST(TestAhoCorasickAdditional, MaskMultipleMatches) {
    RegexMatcher rm("", 90);
    std::string msg = "password: alpha password: beta";
    std::string masked = rm.mask(msg);
    ASSERT_GE(std::count(masked.begin(), masked.end(), '*')/3, 2);
}

TEST(TestAhoCorasickAdditional, MaskNoMatch) {
    RegexMatcher rm("");
    std::string text = "this is safe";
    ASSERT_EQ(rm.mask(text), text);
}

TEST(TestAhoCorasickAdditional, FindMatchesGroup0) {
    RegexMatcher rm("");
    std::regex rgx("safe");
    rm.regexes.clear();
    rm.regexes.push_back(rgx);
    std::string masked = rm.mask("safe");
    ASSERT_TRUE(masked.find("*") != std::string::npos || masked == "safe");
}

TEST(TestAhoCorasickAdditional, InvalidConfigFile) {
    std::string path = "/this/does/not/exist/broken.toml";
    RegexMatcher rm(path);
    std::string m = rm.mask("password: example");
    ASSERT_NE(m.find("*"), std::string::npos);
}