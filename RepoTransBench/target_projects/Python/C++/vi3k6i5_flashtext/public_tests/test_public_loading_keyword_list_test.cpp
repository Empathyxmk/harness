#include <gtest/gtest.h>
#include <string>
#include <vector>
#include "../../include/keyword_processor.h"

TEST(PublicLoadingKeywordList, LoadKeywordListVector) {
    KeywordProcessor kp;
    std::vector<std::string> keys = {"php", "r"};
    for (const auto& k : keys) kp.addKeyword(k);
    auto found = kp.extractKeywords("php r");
    ASSERT_EQ(found.size(), 2);
    EXPECT_EQ(found[0], "php");
    EXPECT_EQ(found[1], "r");
}