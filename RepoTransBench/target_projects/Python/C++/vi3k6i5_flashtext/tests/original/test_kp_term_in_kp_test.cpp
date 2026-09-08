#include <gtest/gtest.h>
#include "../../include/keyword_processor.h"

TEST(KpTermInKp, ContainsKeyword) {
    KeywordProcessor kp;
    kp.addKeyword("rust");
    EXPECT_TRUE(kp.hasKeyword("rust"));
    EXPECT_FALSE(kp.hasKeyword("go"));
}