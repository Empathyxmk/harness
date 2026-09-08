#include <gtest/gtest.h>
#include <algorithm>
#include "wikipedia_api_mock.h"

TEST(PublicUtilsAndConstsTest, ConstantsTypesAndValues) {
    EXPECT_TRUE(typeid(USER_AGENT) == typeid(std::string));
    std::string lower = USER_AGENT;
    std::transform(lower.begin(), lower.end(), lower.begin(), ::tolower);
    EXPECT_NE(lower.find("wikipedia"), std::string::npos);
    EXPECT_TRUE(typeid(MIN_USER_AGENT_LEN) == typeid(int));
    EXPECT_GT(MIN_USER_AGENT_LEN, 0);
    EXPECT_GT(MAX_LANG_LEN, 1);
}

TEST(PublicUtilsAndConstsTest, PublicReSectionPatternsOther) {
    // For HTML (should contain substr), for WIKI (should contain substr)
    EXPECT_NE(RE_SECTION.at(ExtractFormat::HTML).pattern().find("\\n? *<h([1-9])"), std::string::npos);
    EXPECT_NE(RE_SECTION.at(ExtractFormat::WIKI).pattern().find("\\n\\n"), std::string::npos);
}