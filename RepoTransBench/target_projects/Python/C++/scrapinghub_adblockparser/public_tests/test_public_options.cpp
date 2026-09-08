#include <gtest/gtest.h>
#include "adblockparser.h"

TEST(PublicOptionsTest, ParseOptionsSimple) {
    AdblockRule r("/ad.js$script,domain=example.com|another.net");
    auto opts = r.options();
    ASSERT_TRUE(opts.find("script") != opts.end());
    ASSERT_TRUE(opts.find("domain") != opts.end());
    auto doms = std::any_cast<std::set<std::string>>(opts["domain"]);
    std::set<std::string> expected = {"example.com", "another.net"};
    EXPECT_EQ(doms, expected);
}

TEST(PublicOptionsTest, ParseOptionsNoOptions) {
    AdblockRule r("/track.gif");
    auto opts = r.options();
    EXPECT_TRUE(opts.empty());
}

TEST(PublicOptionsTest, ParseOptionsComplex) {
    AdblockRule r("/analytics.js$image,third-party,domain=mysite.org|anothersite.co.uk");
    auto opts = r.options();
    ASSERT_TRUE(opts.find("image") != opts.end());
    ASSERT_TRUE(opts.find("third-party") != opts.end());
    auto doms = std::any_cast<std::set<std::string>>(opts["domain"]);
    std::set<std::string> expected = {"mysite.org", "anothersite.co.uk"};
    EXPECT_EQ(doms, expected);
}

TEST(PublicOptionsTest, ParseOptionsException) {
    AdblockRule r("@@/nocache.png$subdocument,domain=sub.example.org");
    EXPECT_TRUE(r.is_exception());
    auto opts = r.options();
    ASSERT_TRUE(opts.find("subdocument") != opts.end());
    auto doms = std::any_cast<std::set<std::string>>(opts["domain"]);
    std::set<std::string> expected = {"sub.example.org"};
    EXPECT_EQ(doms, expected);
}