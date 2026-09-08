#include <gtest/gtest.h>
#include <vector>
#include <string>
#include "../../include/keyword_processor.h"

TEST(LoadingKeywordList, AddKeywordList) {
    KeywordProcessor kp;
    std::vector<std::string> keywords = {"haskell", "erlang", "elixir"};
    for (const auto& k : keywords) kp.addKeyword(k);
    auto found = kp.extractKeywords("haskell elixir");
    ASSERT_EQ(found.size(), 2);
    EXPECT_EQ(found[0], "haskell");
    EXPECT_EQ(found[1], "elixir");
}