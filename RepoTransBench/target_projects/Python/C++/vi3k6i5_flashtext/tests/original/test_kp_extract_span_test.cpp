#include <gtest/gtest.h>
#include <string>
#include <utility>
#include <vector>
#include "../../include/keyword_processor.h"

TEST(KpExtractSpan, ReturnsKeywordSpans) {
    KeywordProcessor kp;
    kp.addKeyword("python");
    kp.addKeyword("java");
    std::vector<std::pair<std::string, std::pair<size_t, size_t>>> spans;
    std::string text = "I love python and java.";
    spans = kp.extractKeywordSpans(text); // Should return [(python, (7, 13)), (java, (18, 22))]

    ASSERT_EQ(spans.size(), 2);
    EXPECT_EQ(spans[0].first, "python");
    EXPECT_EQ(spans[0].second.first, 7u);
    EXPECT_EQ(spans[0].second.second, 13u);
    EXPECT_EQ(spans[1].first, "java");
    EXPECT_EQ(spans[1].second.first, 18u);
    EXPECT_EQ(spans[1].second.second, 22u);
}