#include <gtest/gtest.h>
#include <string>
#include <algorithm>
// #include "main.h"
std::string process_input(const std::string& s) {
    std::string rev = s;
    std::reverse(rev.begin(), rev.end());
    if (rev == s) return s;
    return rev;
}
TEST(PublicMainTest, ProcessInputReverse) {
    EXPECT_EQ(process_input("alpha"), "ahpla");
}
TEST(PublicMainTest, ProcessInputPalindrome) {
    EXPECT_EQ(process_input("noon"), "noon");
}