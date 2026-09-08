#include <gtest/gtest.h>
#include "claude_to_chatgpt/util.h"

class UtilTest : public ::testing::Test {};

// Basic non-empty string returns correct token count
TEST_F(UtilTest, NumTokensFromStringBasic) {
    num_tokens_from_string_patch = [](const std::string&) { return 3; };
    EXPECT_EQ(num_tokens_from_string("abc"), 3);
}

// Empty string case
TEST_F(UtilTest, NumTokensFromStringEmpty) {
    num_tokens_from_string_patch = [](const std::string&) { return 0; };
    EXPECT_EQ(num_tokens_from_string(""), 0);
}