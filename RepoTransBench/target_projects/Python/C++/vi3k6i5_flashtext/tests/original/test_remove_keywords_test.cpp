#include <gtest/gtest.h>
#include "../../include/keyword_processor.h"

TEST(RemoveKeywords, RemoveAndCheck) {
    KeywordProcessor kp;
    kp.addKeyword("java");
    kp.addKeyword("python");
    EXPECT_TRUE(kp.hasKeyword("java"));
    kp.removeKeyword("java");
    EXPECT_FALSE(kp.hasKeyword("java"));
    EXPECT_TRUE(kp.hasKeyword("python"));
}