#include <gtest/gtest.h>
#include <stdexcept>
#include "../../include/keyword_processor.h"

TEST(PublicExceptions, EmptyKeywordThrows) {
    KeywordProcessor kp;
    EXPECT_THROW(kp.addKeyword(""), std::invalid_argument);
}