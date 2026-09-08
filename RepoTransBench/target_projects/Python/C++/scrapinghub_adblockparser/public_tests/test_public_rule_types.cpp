#include <gtest/gtest.h>
#include "adblockparser.h"

TEST(PublicRuleTypesTest, PublicIsComment) {
    std::vector<std::string> COMMENT_RULES = {
        "! This is a comment line",
        "! Title: Example Filter List",
        "! Expires: 4 days",
        "! Homepage: https://example.com/",
        "[Adblock]",
        "!#include another_list.txt"
    };
    for(const auto& text : COMMENT_RULES) {
        AdblockRule rule(text);
        EXPECT_TRUE(rule.is_comment());
        EXPECT_FALSE(rule.is_html_rule());
        EXPECT_FALSE(rule.is_exception());
        EXPECT_TRUE(rule.options().empty());
        EXPECT_FALSE(rule.has_regex());
    }
}

TEST(PublicRuleTypesTest, PublicIsHtmlRule) {
    std::vector<std::string> HTML_RULES = {
        "##.bannerAd",
        "@@##.sponsoredContent",
        "mysite.com#@##sidebar",
        "@@##.cookieBar",
        "example.net,example.org#@##promo",
        "##a[href^='https://tracker.example.com/']",
        "##img[src$='.ads.png']"
    };
    for(const auto& text : HTML_RULES) {
        AdblockRule rule(text);
        EXPECT_TRUE(rule.is_html_rule());
        EXPECT_FALSE(rule.is_comment());
    }
}