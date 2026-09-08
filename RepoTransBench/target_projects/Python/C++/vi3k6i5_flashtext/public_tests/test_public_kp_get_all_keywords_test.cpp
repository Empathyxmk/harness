#include <gtest/gtest.h>
#include <vector>
#include <string>
#include "../../include/keyword_processor.h"

TEST(PublicGetKeywords, AllAddedArePresent) {
    KeywordProcessor kp;
    kp.addKeyword("haskell");
    kp.addKeyword("lua");
    auto all = kp.getAllKeywords();
    EXPECT_NE(std::find(all.begin(), all.end(), "haskell"), all.end());
    EXPECT_NE(std::find(all.begin(), all.end(), "lua"), all.end());
}