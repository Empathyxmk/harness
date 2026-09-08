#include <gtest/gtest.h>
#include "version_part.h"

TEST(PublicVersionPart, ValueSetting) {
    VersionPart vp("7");
    EXPECT_EQ(vp.str(), "7");
}

TEST(PublicVersionPart, CompareDifferentValues) {
    VersionPart vp1("3");
    VersionPart vp2("10");
    EXPECT_NE(vp1, vp2);
}

TEST(PublicVersionPart, EqualityWithSameValue) {
    VersionPart vp1("hello");
    VersionPart vp2("hello");
    EXPECT_EQ(vp1, vp2);
}

TEST(PublicVersionPart, Repr) {
    VersionPart vp("2024");
    std::ostringstream oss;
    oss << vp;
    EXPECT_NE(oss.str().find("2024"), std::string::npos);
}

TEST(PublicVersionPart, StrCast) {
    VersionPart vp("543");
    EXPECT_EQ(vp.str(), "543");
}

TEST(PublicVersionPart, IntCast) {
    VersionPart vp("8");
    EXPECT_EQ(std::stoi(vp.value), 8);
}

TEST(PublicVersionPart, IntCastNonNumeric) {
    VersionPart vp("xyz");
    EXPECT_THROW(std::stoi(vp.value), std::invalid_argument);
}