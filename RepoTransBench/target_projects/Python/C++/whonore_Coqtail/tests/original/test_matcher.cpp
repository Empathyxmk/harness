#include <gtest/gtest.h>
#include <regex>
#include <string>

// Imaginary pattern matcher similar to what's used in Python
bool matcher(const std::string& str, const std::string& pattern) {
    std::regex re(pattern);
    return std::regex_search(str, re);
}

TEST(MatcherTest, SimpleMatch) {
    EXPECT_TRUE(matcher("Goal nat.", "^Goal"));
}

TEST(MatcherTest, NoMatch) {
    EXPECT_FALSE(matcher("Lemma foo.", "^Goal"));
}

TEST(MatcherTest, RegexMatch) {
    EXPECT_TRUE(matcher("Inductive foo : nat -> Prop.", "Inductive [a-z]+ : nat.*"));
}