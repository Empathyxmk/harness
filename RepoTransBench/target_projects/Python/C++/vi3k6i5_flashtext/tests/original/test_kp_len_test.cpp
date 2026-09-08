#include <gtest/gtest.h>
#include "../../include/keyword_processor.h"

TEST(KpLen, LengthZeroInitially) {
    KeywordProcessor kp;
    EXPECT_EQ(kp.keywordCount(), 0u);
}

TEST(KpLen, LengthAfterAdding) {
    KeywordProcessor kp;
    kp.addKeyword("java");
    kp.addKeyword("python");
    EXPECT_EQ(kp.keywordCount(), 2u);
}