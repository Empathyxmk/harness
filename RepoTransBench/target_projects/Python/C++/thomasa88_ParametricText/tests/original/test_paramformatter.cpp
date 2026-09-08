#include <gtest/gtest.h>
#include "paramformatter.h"

struct DummyParam : public Param {
    DummyParam(double v, std::string u) : Param(v, u) {}
};

struct DummyDesignAdapter : public DummyDesign {};

class TestMixedFracInch : public ::testing::Test {
protected:
    DummyDesignAdapter design;
};

TEST_F(TestMixedFracInch, UnitlessPositive) {
    DummyParam p(1.75, "");
    EXPECT_EQ(mixed_frac_inch(p, &design), "1 3/4\"");
}

TEST_F(TestMixedFracInch, UnitlessNegative) {
    DummyParam p(-2.5, "");
    EXPECT_EQ(mixed_frac_inch(p, &design), "-2 1/2\"");
}

TEST_F(TestMixedFracInch, UnitInch) {
    DummyParam p(2.5, "in");
    EXPECT_EQ(mixed_frac_inch(p, &design), "2 1/2\"");
}

TEST_F(TestMixedFracInch, WholeNumber) {
    DummyParam p(3.0, "");
    EXPECT_EQ(mixed_frac_inch(p, &design), "3\"");
    DummyParam p0(0.0, "");
    EXPECT_EQ(mixed_frac_inch(p0, &design), "0\"");
}

TEST_F(TestMixedFracInch, FractionOnly) {
    DummyParam p(0.25, "");
    EXPECT_EQ(mixed_frac_inch(p, &design), "1/4\"");
    DummyParam pn(-0.75, "");
    EXPECT_EQ(mixed_frac_inch(pn, &design), "-3/4\"");
}

TEST_F(TestMixedFracInch, Zero) {
    DummyParam p(0, "");
    EXPECT_EQ(mixed_frac_inch(p, &design), "0\"");
}