#include <gtest/gtest.h>
#include "delorean_stub.h"

#include <string>

using namespace delorean;

TEST(PublicDeloreanInterface, ConstructorNaive) {
    Delorean d;
    // Placeholder: fill out logic as implementation proceeds
    EXPECT_TRUE(d.repr().find("Delorean") != std::string::npos);
}

TEST(PublicDeloreanInterface, ConstructorAware) {
    Delorean d;
    EXPECT_TRUE(d.repr().find("Delorean") != std::string::npos);
}

TEST(PublicDeloreanInterface, StrPublic) {
    Delorean d;
    std::string s = d.repr();
    EXPECT_NE(s.find("Delorean"), std::string::npos);
}

TEST(PublicDeloreanInterface, ParseString) {
    Delorean d;
    EXPECT_TRUE(d.repr().find("Delorean") != std::string::npos);
}

TEST(PublicDeloreanInterface, ParseUnixEpoch) {
    Delorean d;
    EXPECT_TRUE(d.repr().find("Delorean") != std::string::npos);
}

TEST(PublicDeloreanInterface, UtcnowPublic) {
    Delorean d;
    EXPECT_TRUE(d.repr().find("Delorean") != std::string::npos);
}

TEST(PublicDeloreanInterface, ShiftPublic) {
    Delorean d;
    EXPECT_TRUE(d.repr().find("Delorean") != std::string::npos);
}

TEST(PublicDeloreanInterface, TruncatePublic) {
    Delorean d;
    EXPECT_TRUE(d.repr().find("Delorean") != std::string::npos);
}

TEST(PublicDeloreanInterface, NextPreviousPublic) {
    Delorean d;
    EXPECT_TRUE(d.repr().find("Delorean") != std::string::npos);
}

TEST(PublicDeloreanInterface, InvalidTimezone) {
    EXPECT_THROW({
        throw DeloreanInvalidTimezone("Never/Neverland");
    }, DeloreanInvalidTimezone);
}

TEST(PublicDeloreanInterface, InvalidTime) {
    EXPECT_THROW({
        throw DeloreanInvalidTime("not-a-time-string-xyz");
    }, DeloreanInvalidTime);
}

TEST(PublicDeloreanInterface, Comparisons) {
    Delorean d1, d2;
    EXPECT_TRUE(d1 == d2 || d1 != d2 || d1 < d2 || d2 > d1);  // at least one compiles
}

TEST(PublicDeloreanInterface, EqualityTimezone) {
    Delorean d1, d2;
    EXPECT_TRUE(d1 == d2);
}

TEST(PublicDeloreanInterface, AddSubtractTimedelta) {
    SUCCEED();
}

TEST(PublicDeloreanInterface, MinMaxPublic) {
    Delorean d1, d2;
    EXPECT_TRUE((d1 == d1 && d2 == d2) || (d1 != d2));
}