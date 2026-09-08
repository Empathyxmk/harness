#include <gtest/gtest.h>
#include "adblockparser.h"
#include <map>
#include <string>

TEST(AdblockOptionsTest, SplitOptions) {
    struct Case {
        std::string text;
        std::vector<std::string> result;
    };
    std::vector<Case> cases = {
        {"subdocument,third-party", {"subdocument", "third-party"}},
        {"object-subrequest,script,domain=~msnbc.msn.com,~www.nbcnews.com",
         {"object-subrequest", "script", "domain=~msnbc.msn.com,~www.nbcnews.com"}},
        {"object-subrequest,script,domain=~msnbc.msn.com,~www.nbcnews.com",
         {"object-subrequest", "script", "domain=~msnbc.msn.com,~www.nbcnews.com"}},
        {"~document,xbl,domain=~foo,bar,baz,~collapse,domain=foo.xbl|bar",
         {"~document", "xbl", "domain=~foo,bar,baz", "~collapse", "domain=foo.xbl|bar"}},
        {"domain=~example.com,foo.example.com,script",
         {"domain=~example.com,foo.example.com", "script"}},
    };
    for(const auto& c : cases) {
        EXPECT_EQ(AdblockRule::_split_options(c.text), c.result);
    }
}

TEST(AdblockOptionsTest, ParseDomainOption) {
    struct Case {
        std::string text;
        std::map<std::string, bool> expected;
    };
    std::vector<Case> cases = {
        {"domain=example.com", {{"example.com", true}}},
        {"domain=example.com|example.net", {{"example.com", true}, {"example.net", true}}},
        {"domain=~example.com", {{"example.com", false}}},
        {"domain=example.com|~foo.example.com", {{"example.com", true}, {"foo.example.com", false}}},
        {"domain=~foo.example.com|example.com", {{"example.com", true}, {"foo.example.com", false}}},
        {"domain=example.com,example.net", {{"example.com", true}, {"example.net", true}}},
        {"domain=example.com|~foo.example.com", {{"example.com", true}, {"foo.example.com", false}}},
        {"domain=~msnbc.msn.com,~www.nbcnews.com", {{"msnbc.msn.com", false}, {"www.nbcnews.com", false}}},
    };
    for(const auto& c : cases) {
        EXPECT_EQ(AdblockRule::_parse_domain_option(c.text), c.expected);
    }
}

TEST(AdblockOptionsTest, OptionsExtraction) {
    struct Case {
        std::string text;
        std::map<std::string, std::any> expected;
    };
    // For now, we use placeholder std::any for values; proper matching with inner maps will be handled in assert logic.
    // Use individual checks below as in original.
    {
        AdblockRule rule("domain=foo.bar");
        EXPECT_EQ(rule.options().size(), 0u);
    }
    {
        AdblockRule rule("+Ads/$~stylesheet");
        auto opts = rule.options();
        ASSERT_TRUE(opts.find("stylesheet") != opts.end());
        EXPECT_EQ(std::any_cast<bool>(opts["stylesheet"]), false);
    }
    {
        AdblockRule rule("-advertising-$domain=~advertise.bingads.domain.com");
        auto opts = rule.options();
        ASSERT_TRUE(opts.find("domain") != opts.end());
        auto doms = std::any_cast<std::map<std::string, bool>>(opts["domain"]);
        ASSERT_TRUE(doms.find("advertise.bingads.domain.com") != doms.end());
        EXPECT_EQ(doms["advertise.bingads.domain.com"], false);
    }
    {
        AdblockRule rule(".se/?placement=$script,third-party");
        auto opts = rule.options();
        ASSERT_TRUE(opts.find("script") != opts.end());
        EXPECT_EQ(std::any_cast<bool>(opts["script"]), true);
        ASSERT_TRUE(opts.find("third-party") != opts.end());
        EXPECT_EQ(std::any_cast<bool>(opts["third-party"]), true);
    }
    {
        AdblockRule rule("||tst.net^$object-subrequest,third-party,domain=domain1.com|domain5.com");
        auto opts = rule.options();
        ASSERT_TRUE(opts.find("object-subrequest") != opts.end());
        EXPECT_EQ(std::any_cast<bool>(opts["object-subrequest"]), true);
        ASSERT_TRUE(opts.find("third-party") != opts.end());
        EXPECT_EQ(std::any_cast<bool>(opts["third-party"]), true);
        ASSERT_TRUE(opts.find("domain") != opts.end());
        auto doms = std::any_cast<std::map<std::string, bool>>(opts["domain"]);
        ASSERT_TRUE(doms.find("domain1.com") != doms.end());
        ASSERT_TRUE(doms.find("domain5.com") != doms.end());
        EXPECT_EQ(doms["domain1.com"], true);
        EXPECT_EQ(doms["domain5.com"], true);
    }
}