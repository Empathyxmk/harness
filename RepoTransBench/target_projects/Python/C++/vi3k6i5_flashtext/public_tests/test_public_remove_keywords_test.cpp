#include <gtest/gtest.h>
#include <string>
#include "../../include/keyword_processor.h"

TEST(PublicRemoveKeywords, RemoveKeywordWorks) {
    KeywordProcessor kp;
    kp.addKeyword("scala");
    kp.addKeyword("javascript");
    kp.removeKeyword("scala");
    EXPECT_FALSE(kp.hasKeyword("scala"));
    EXPECT_TRUE(kp.hasKeyword("javascript"));
}