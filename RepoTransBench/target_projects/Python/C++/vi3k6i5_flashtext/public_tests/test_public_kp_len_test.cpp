#include <gtest/gtest.h>
#include "../../include/keyword_processor.h"

TEST(PublicLen, KeywordCountWorks) {
    KeywordProcessor kp;
    EXPECT_EQ(kp.keywordCount(), 0u);
    kp.addKeyword("scala");
    EXPECT_EQ(kp.keywordCount(), 1u);
}