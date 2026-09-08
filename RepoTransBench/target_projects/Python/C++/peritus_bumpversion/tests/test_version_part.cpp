#include <gtest/gtest.h>
#include "version_part.h"

struct ConfFixture {
    std::string first_value;
};

class VersionPartConfVPC : public ::testing::TestWithParam<ConfFixture> {};

INSTANTIATE_TEST_SUITE_P(
    VersionPartParams,
    VersionPartConfVPC,
    ::testing::Values(
        ConfFixture{ "0" },
        ConfFixture{ "1" },
        ConfFixture{ "3" }
    )
);

TEST_P(VersionPartConfVPC, Init) {
    auto c = GetParam();
    VersionPart vp(c.first_value);
    EXPECT_EQ(vp.value, c.first_value);
}

TEST_P(VersionPartConfVPC, Copy) {
    auto c = GetParam();
    VersionPart vp(c.first_value);
    VersionPart vc = vp.copy();
    EXPECT_EQ(vp.value, vc.value);
}

TEST_P(VersionPartConfVPC, Bump) {
    auto c = GetParam();
    VersionPart vp(c.first_value);
    VersionPart vc = vp.bump();
    EXPECT_EQ(vc.value, std::to_string(std::stoi(c.first_value) + 1));
}

TEST_P(VersionPartConfVPC, OptionalFalseAfterBump) {
    auto c = GetParam();
    VersionPart vp(c.first_value);
    EXPECT_FALSE(vp.bump().is_optional());
}

TEST_P(VersionPartConfVPC, OptionalTrueOnCreation) {
    auto c = GetParam();
    VersionPart vp(c.first_value);
    EXPECT_TRUE(vp.is_optional());
}

TEST_P(VersionPartConfVPC, FormatWorks) {
    auto c = GetParam();
    VersionPart vp(c.first_value);
    std::ostringstream oss;
    oss << vp;
    EXPECT_EQ(oss.str(), c.first_value);
}

TEST_P(VersionPartConfVPC, Equality) {
    auto c = GetParam();
    VersionPart vp1(c.first_value);
    VersionPart vp2(c.first_value);
    EXPECT_EQ(vp1, vp2);
}

TEST_P(VersionPartConfVPC, NullEqualsNull) {
    auto c = GetParam();
    VersionPart vp(c.first_value);
    EXPECT_EQ(vp.null().value, VersionPart("0").value);
}