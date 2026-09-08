#include <gtest/gtest.h>
#include "version_part.h"

TEST(PublicVersionPartExtra, HasValue) {
    VersionPart vp("nonempty");
    EXPECT_FALSE(vp.value.empty());
}

TEST(PublicVersionPartExtra, NotHasValueEmptyString) {
    VersionPart vp("");
    EXPECT_TRUE(vp.value.empty());
}

TEST(PublicVersionPartExtra, IntCastZero) {
    VersionPart vp("0");
    EXPECT_EQ(std::stoi(vp.value), 0);
}

TEST(PublicVersionPartExtra, IgnoreValue) {
    VersionPart vp("ignored");
    EXPECT_EQ(vp.value, "ignored");
}

TEST(PublicVersionPartExtra, ReprContainsClass) {
    VersionPart vp("classy");
    std::ostringstream oss;
    oss << vp;
    EXPECT_NE(oss.str().find("classy"), std::string::npos);
}