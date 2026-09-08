#include <gtest/gtest.h>
#include "adblockparser.h"
#include <vector>
#include <string>

TEST(AdblockRuleTypesTest, IsComment) {
    std::vector<std::string> COMMENT_RULES = {
        "[Adblock Plus 2.0]",
        "! Checksum: nVIXktYXKU6M+cu+Txkhuw",
        "!/cb.php?sub$script,third-party",
        "!@@/cb.php?sub",
        "!###ADSLOT_SKYSCRAPER",
        "! *** easylist:easylist/easylist_whitelist_general_hide.txt ***"
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

TEST(AdblockRuleTypesTest, IsHtmlRule) {
    std::vector<std::string> HTML_RULES = {
        "###ADSLOT_SKYSCRAPER",
        "@@###ADSLOT_SKYSCRAPER",
        "##.adsBox",
        "eee.se#@##adspace_top",
        "domain1.com,domain2.com#@##adwrapper",
        "edgesuitedomain.net#@##ad-unit",
        "mydomain.com#@#.ad-unit",
        "##a[href^=\"http://affiliate.sometracker.com/\"]"
    };
    for(const auto& text : HTML_RULES) {
        AdblockRule rule(text);
        EXPECT_TRUE(rule.is_html_rule());
        EXPECT_FALSE(rule.is_comment());
    }
}