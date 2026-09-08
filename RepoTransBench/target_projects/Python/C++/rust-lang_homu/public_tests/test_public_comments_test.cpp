#include <gtest/gtest.h>
#include <string>
#include <regex>
// #include "comments.h"

// Strip @user from start, leaving the rest and trimming spaces
std::string strip_mention(const std::string& msg) {
    std::regex mention_re("^\\s*@\\w+\\s+");
    return std::regex_replace(msg, mention_re, "");
}

TEST(PublicCommentsTest, StripMentionFromMessage) {
    std::string msg1 = "@botuser please test";
    EXPECT_EQ(strip_mention(msg1), "please test");
    std::string msg2 = "  @dev hello Homu!**  ";
    EXPECT_EQ(strip_mention(msg2), "hello Homu!**  ");
}