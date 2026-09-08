#include <gtest/gtest.h>
#include "../../include/keyword_processor.h"

TEST(PublicTermInKP, CanCheckMembership) {
    KeywordProcessor kp;
    kp.addKeyword("typescript");
    EXPECT_TRUE(kp.hasKeyword("typescript"));
    EXPECT_FALSE(kp.hasKeyword("perl"));
}