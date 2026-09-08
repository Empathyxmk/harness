#include <gtest/gtest.h>
#include <vector>
#include <string>
#include "../../include/keyword_processor.h"

TEST(PublicNextWord, IteratorWorks) {
    KeywordProcessor kp;
    kp.addKeyword("erlang");
    kp.addKeyword("elixir");
    auto iter = kp.begin();
    ASSERT_NE(iter, kp.end());
    EXPECT_EQ(*iter, "erlang");
    ++iter;
    ASSERT_NE(iter, kp.end());
    EXPECT_EQ(*iter, "elixir");
}