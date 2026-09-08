#include <gtest/gtest.h>
#include "adblockparser.h"

TEST(PublicParsingTest, PublicBlockScript) {
    std::vector<std::string> rules = {
        "/track.js$script",
        "/log.gif$image",
        "||adnetwork.com^$third-party",
        "@@||safe.com/banner.gif$image"
    };
    AdblockRules adp(rules);
    EXPECT_TRUE(adp.should_block("http://another.com/track.js", {{"script", true}}));
    EXPECT_FALSE(adp.should_block("http://another.com/track.js", {{"image", true}}));
}

TEST(PublicParsingTest, PublicBlockImage) {
    std::vector<std::string> rules = {
        "/track.js$script",
        "/log.gif$image",
        "||adnetwork.com^$third-party",
        "@@||safe.com/banner.gif$image"
    };
    AdblockRules adp(rules);
    EXPECT_FALSE(adp.should_block("http://foo.com/track.gif", {{"image", true}}));
    EXPECT_TRUE(adp.should_block("http://foo.com/log.gif", {{"image", true}}));
}

TEST(PublicParsingTest, PublicThirdParty) {
    std::vector<std::string> rules = {
        "/track.js$script",
        "/log.gif$image",
        "||adnetwork.com^$third-party",
        "@@||safe.com/banner.gif$image"
    };
    AdblockRules adp(rules);
    EXPECT_FALSE(adp.should_block("http://x.yz/ad.js", {{"third-party", true}}));
    EXPECT_TRUE(adp.should_block("http://adnetwork.com/adv_banner.jpg", {{"third-party", true}}));
}

TEST(PublicParsingTest, PublicException) {
    std::vector<std::string> rules = {
        "/track.js$script",
        "/log.gif$image",
        "||adnetwork.com^$third-party",
        "@@||safe.com/banner.gif$image"
    };
    AdblockRules adp(rules);
    EXPECT_FALSE(adp.should_block("http://safe.com/banner.gif", {{"image", true}}));
}