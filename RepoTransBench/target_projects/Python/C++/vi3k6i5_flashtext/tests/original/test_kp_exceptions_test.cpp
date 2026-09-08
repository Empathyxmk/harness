#include <gtest/gtest.h>
#include "../../include/keyword_processor.h"

TEST(KpExceptions, ThrowsWhenKeywordIsEmpty) {
    KeywordProcessor kp;
    EXPECT_THROW(kp.addKeyword(""), std::invalid_argument);
}

TEST(KpExceptions, ThrowsWhenExtractWithoutKeywords) {
    KeywordProcessor kp;
    EXPECT_THROW(kp.extractKeywords("test string"), std::logic_error);
}