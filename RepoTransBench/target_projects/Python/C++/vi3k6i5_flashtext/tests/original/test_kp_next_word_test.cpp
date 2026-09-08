#include <gtest/gtest.h>
#include "../../include/keyword_processor.h"

TEST(KpNextWord, ReturnsWordsInCorrectOrder) {
    KeywordProcessor kp;
    kp.addKeyword("java");
    kp.addKeyword("python");
    kp.addKeyword("ruby");

    auto iter = kp.begin();
    ASSERT_NE(iter, kp.end());
    EXPECT_EQ(*iter, "java");
    ++iter;
    ASSERT_NE(iter, kp.end());
    EXPECT_EQ(*iter, "python");
    ++iter;
    ASSERT_NE(iter, kp.end());
    EXPECT_EQ(*iter, "ruby");
}