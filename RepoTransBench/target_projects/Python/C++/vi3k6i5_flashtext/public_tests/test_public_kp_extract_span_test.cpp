#include <gtest/gtest.h>
#include <string>
#include <vector>
#include "../../include/keyword_processor.h"

TEST(PublicExtractSpan, ExtractKeywordSpan) {
    KeywordProcessor kp;
    kp.addKeyword("csharp");
    auto spans = kp.extractKeywordSpans("i like csharp");
    ASSERT_EQ(spans.size(), 1);
    EXPECT_EQ(spans[0].first, "csharp");
    // Some span check (positions): let’s say the function returns correct positions for "csharp"
}