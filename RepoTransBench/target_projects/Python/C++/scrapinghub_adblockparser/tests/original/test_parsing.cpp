#include <gtest/gtest.h>
#include <stdexcept>
#include <string>
#include <vector>
#include <map>
#include <memory>
#include "adblockparser.h"  // You need to implement Rule, RuleList, etc.

// Helper utilities for test
struct RuleTestCase {
    std::string rule_text;
    std::string expected_type;
    std::string expected_pattern;
    std::map<std::string, bool> expected_options;
    std::vector<std::string> expected_domains;
    std::vector<std::string> expected_blocked_domains;
    bool is_exception = false;
    bool is_html_rule = false;
};

TEST(RuleParsing, DocumentedTests) {
    // Each example from Adblock Plus documentation
    std::vector<RuleTestCase> tests = {
        {"||example.com^", "url_pattern", "||example.com^", {}, {}, {}, false, false},
        {"@@||example.com^", "url_pattern", "||example.com^", {}, {}, {}, true, false},
        {"/adimage*.gif", "url_pattern", "/adimage*.gif", {}, {}, {}, false, false},
        {"example.com/banner*", "url_pattern", "example.com/banner*", {}, {}, {}, false, false},
        {"@@/adimage*.gif", "url_pattern", "/adimage*.gif", {}, {}, {}, true, false},
        {"! This is a comment", "comment", "", {}, {}, {}, false, false},
        {"[Adblock Plus 1.1]", "header", "", {}, {}, {}, false, false}
    };

    for (const auto& t : tests) {
        Rule rule(t.rule_text);
        EXPECT_EQ(rule.type(), t.expected_type);
        EXPECT_EQ(rule.pattern(), t.expected_pattern);
        EXPECT_EQ(rule.is_exception(), t.is_exception);
    }
}

TEST(RuleParsing, RuleExceptions) {
    Rule r1("@@/adimage*.gif");
    EXPECT_TRUE(r1.is_exception());

    Rule r2("||example.com^");
    EXPECT_FALSE(r2.is_exception());
}

TEST(RuleParsing, RuleWithOptions) {
    Rule r("||example.com^$script,image,domain=example.com|~foo.example.com");
    EXPECT_EQ(r.type(), "url_pattern");
    EXPECT_EQ(r.pattern(), "||example.com^");
    EXPECT_TRUE(r.option("script"));
    EXPECT_TRUE(r.option("image"));
    EXPECT_EQ(r.domains(), std::vector<std::string>({"example.com"}));
    EXPECT_EQ(r.blocked_domains(), std::vector<std::string>({"foo.example.com"}));
}

TEST(RuleParsing, MultirulesWithOptions) {
    std::vector<std::string> rules = {
        "||example.com^$script,domain=foo.com|~bar.com",
        "||example.org^$image,domain=bar.com|~baz.com",
    };

    std::vector<std::string> expected_patterns = {
        "||example.com^",
        "||example.org^",
    };

    std::vector<std::string> expected_options = {
        "script",
        "image",
    };

    for (size_t i = 0; i < rules.size(); ++i) {
        Rule r(rules[i]);
        EXPECT_EQ(r.pattern(), expected_patterns[i]);
        EXPECT_TRUE(r.option(expected_options[i]));
    }
}

TEST(RuleParsing, RegexpRules) {
    Rule r("/adimage\\d+\\.gif/");
    EXPECT_EQ(r.type(), "regexp");
    EXPECT_EQ(r.pattern(), "/adimage\\d+\\.gif/");
}

TEST(RuleParsing, RuleSupportedOptions) {
    Rule r("||example.com^$script,image,third-party,subdocument,xmlhttprequest,popup");
    EXPECT_TRUE(r.option("script"));
    EXPECT_TRUE(r.option("image"));
    EXPECT_TRUE(r.option("third-party"));
    EXPECT_TRUE(r.option("subdocument"));
    EXPECT_TRUE(r.option("xmlhttprequest"));
    EXPECT_TRUE(r.option("popup"));
    EXPECT_FALSE(r.option("stylesheet"));
}

TEST(RuleParsing, RuleInstantiation) {
    // This test is mainly to make sure rules can be instantiated with typical inputs.
    std::vector<std::string> inputs = {
        "||example.com^",
        "bla$script",
        "/imgad.jpg/",
        "! comment",
        "[Adblock plus 1.1]",
        "||another.com^$image,~popup,domain=foo.com|~bar.com"
    };
    for (const auto& s : inputs) {
        Rule r(s);
        // Just check it doesn't throw and has a type
        EXPECT_FALSE(r.type().empty());
    }
}

TEST(RuleParsing, EmptyRules) {
    Rule r1("");
    EXPECT_EQ(r1.type(), "unknown");
    Rule r2(" ");
    EXPECT_EQ(r2.type(), "unknown");
    Rule r3("    ");
    EXPECT_EQ(r3.type(), "unknown");
}

TEST(RuleParsing, EmptyRegexpRuleThrows) {
    EXPECT_THROW({
        Rule r("/");
    }, std::runtime_error);

    EXPECT_THROW({
        Rule r("/  /");
    }, std::runtime_error);
}

TEST(RuleParsing, RuleOptionWithNoValueThrows) {
    EXPECT_THROW({
        Rule r("||example.com^$domain=");
    }, std::runtime_error);
}

TEST(RuleParsing, UnknownOptionDoesNotThrow) {
    Rule r("||example.com^$foobar");
    // Unknown options do not throw, but option("foobar") should be true if set
    EXPECT_TRUE(r.option("foobar"));
}

TEST(RuleParsing, CommentsAndHeadersAreParsed) {
    Rule r1("! this is a comment");
    EXPECT_EQ(r1.type(), "comment");

    Rule r2("[Adblock Plus 1.1]");
    EXPECT_EQ(r2.type(), "header");
}

TEST(RuleParsing, ExceptionRuleWithOptions) {
    Rule r("@@||foo.com^$script,domain=bar.com|~baz.com");
    EXPECT_TRUE(r.is_exception());
    EXPECT_TRUE(r.option("script"));
    EXPECT_EQ(r.domains(), std::vector<std::string>({"bar.com"}));
    EXPECT_EQ(r.blocked_domains(), std::vector<std::string>({"baz.com"}));
}

TEST(RuleParsing, DomainAndBlockedDomainsAreExtracted) {
    Rule r("||example.com^$domain=foo.com|~bar.com|baz.com|~qux.com");
    std::vector<std::string> expected_domains = {"foo.com", "baz.com"};
    std::vector<std::string> expected_blocked = {"bar.com", "qux.com"};
    EXPECT_EQ(r.domains(), expected_domains);
    EXPECT_EQ(r.blocked_domains(), expected_blocked);
}

TEST(RuleParsing, IgnoreMalformedBlockedDomainList) {
    // If domain= is malformed it should not throw but may ignore some parts
    Rule r("||example.com^$domain=|~|,|");
    // Should be empty (ignores all)
    EXPECT_TRUE(r.domains().empty());
    EXPECT_TRUE(r.blocked_domains().empty());
}

TEST(RuleParsing, RuleWithUnknownOptionDoesNotAffectKnownOptions) {
    Rule r("||example.com^$script,foobar");
    EXPECT_TRUE(r.option("script"));
    EXPECT_TRUE(r.option("foobar"));
}

TEST(RuleParsing, OptionParsingWithWhitespaceTrim) {
    Rule r("||example.com^$   script  ,   image   ");
    EXPECT_TRUE(r.option("script"));
    EXPECT_TRUE(r.option("image"));
}

TEST(RuleParsing, RuleWithMultipleBlockedDomains) {
    Rule r("||example.com^$domain=foo.com|~bar.com|baz.com|~qux.com");
    std::vector<std::string> expected_domains = {"foo.com", "baz.com"};
    std::vector<std::string> expected_blocked = {"bar.com", "qux.com"};
    EXPECT_EQ(r.domains(), expected_domains);
    EXPECT_EQ(r.blocked_domains(), expected_blocked);
}

// Add more tests here as needed to fully mirror the Python original