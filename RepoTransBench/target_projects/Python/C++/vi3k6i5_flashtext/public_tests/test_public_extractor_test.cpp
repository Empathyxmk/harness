#include <gtest/gtest.h>
#include <string>
#include <vector>
#include "../../include/keyword_processor.h"

TEST(PublicExtractor, ExtractionCase) {
    KeywordProcessor kp;
    kp.addKeyword("rust");
    kp.addKeyword("go");
    std::vector<std::string> res = kp.extractKeywords("I write rust and go");
    ASSERT_EQ(res.size(), 2);
    EXPECT_EQ(res[0], "rust");
    EXPECT_EQ(res[1], "go");
}