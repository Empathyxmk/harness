#include <gtest/gtest.h>
#include <string>
#include <vector>
#include "../../include/keyword_processor.h"

TEST(PublicReplacer, ReplacementHappensForAll) {
    KeywordProcessor kp;
    kp.addKeyword("ruby", "RUBY");
    kp.addKeyword("go", "GO!");
    auto s = kp.replaceKeywords("ruby go");
    EXPECT_EQ(s, "RUBY GO!");
}