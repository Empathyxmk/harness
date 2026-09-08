#include <gtest/gtest.h>
#include <string>
#include <algorithm>
// #include "main.h"

// Placeholder for process_input, pr_body_contains until src logic exists
std::string process_input(const std::string& s) {
    std::string rev = s;
    std::reverse(rev.begin(), rev.end());
    // If palindrome, return as is
    if (rev == s) return s;
    return rev;
}
bool pr_body_contains(const std::string& body, const std::string& key) {
    return body.find(key) != std::string::npos;
}

TEST(MainTest, ProcessInputReverseExisting) {
    EXPECT_EQ(process_input("test"), "tset");
}
TEST(MainTest, ProcessInputPalindromeExisting) {
    EXPECT_EQ(process_input("abba"), "abba");
}