#include <gtest/gtest.h>
#include "version_part.h"

TEST(VersionPartExtra, DefaultBehavior) {
    VersionPart vp("1");
    EXPECT_EQ(vp.value, "1");
    EXPECT_TRUE(vp.is_optional());
    EXPECT_EQ(vp.copy(), vp);
    std::ostringstream oss;
    oss << vp;
    EXPECT_EQ(oss.str(), "1");
    VersionPart vp_bumped = vp.bump();
    EXPECT_EQ(vp_bumped.value, "2");
}

TEST(VersionPartExtra, WithConfigured) {
    VersionPart vp("a"); // No enum bump, so just copies
    EXPECT_EQ(vp.value, "a");
    VersionPart vp2 = vp.bump();
    EXPECT_EQ(vp2.value, "1"); // assume bump falls back to int(0)+1
}

TEST(VersionPartExtra, NullAndEquality) {
    VersionPart vp("4");
    VersionPart null_vp = vp.null();
    EXPECT_EQ(null_vp.value, "0");
    EXPECT_NE(vp, null_vp);
    VersionPart vp2("4");
    EXPECT_EQ(vp, vp2);
}

TEST(VersionPartExtra, ConfigProperties) {
    VersionPart cfg("0");
    EXPECT_EQ(cfg.value, "0");
    EXPECT_TRUE(cfg.is_optional());
    VersionPart bumpd = cfg.bump();
    EXPECT_EQ(bumpd.value, "1");
}