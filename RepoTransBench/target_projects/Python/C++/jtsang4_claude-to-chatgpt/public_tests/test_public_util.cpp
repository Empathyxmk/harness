#include <gtest/gtest.h>
#include "claude_to_chatgpt/util.h"

// Nonempty string, expect 5
TEST(PublicUtilTest, NumTokensFromStringNonempty) {
    num_tokens_from_string_patch = [](const std::string&) { return 5; };
    EXPECT_EQ(num_tokens_from_string("hello"), 5);
}

// Empty string, expect 0
TEST(PublicUtilTest, NumTokensFromStringEmpty) {
    num_tokens_from_string_patch = [](const std::string&) { return 0; };
    EXPECT_EQ(num_tokens_from_string(""), 0);
}