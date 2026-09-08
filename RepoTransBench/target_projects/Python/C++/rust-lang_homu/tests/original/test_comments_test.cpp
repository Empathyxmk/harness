#include <gtest/gtest.h>
#include <string>
#include <regex>
// #include "comments.h"

// Strip @homu or @username prefix (with optional spaces or casing) and leading/trailing spaces
std::string strip_mention(const std::string& msg) {
    std::regex mention_re("^\\s*@\\w+\\s+");
    return std::regex_replace(msg, mention_re, "");
}

TEST(CommentsTest, StripMention) {
    std::string msg1 = "@homu r+";
    EXPECT_EQ(strip_mention(msg1), "r+");
    std::string msg2 = " @Homu  approve please! ";
    EXPECT_EQ(strip_mention(msg2), "approve please!");
}