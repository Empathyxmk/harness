#include <gtest/gtest.h>
#include "functions.h"

TEST(NumericFunctionTestEdge, BasicBump) {
    NumericFunction nf("3");
    EXPECT_EQ(nf.bump("3"), "4");
    EXPECT_EQ(nf.bump("99"), "100");
}

TEST(NumericFunctionTestEdge, FirstAndOptionalValue) {
    NumericFunction nf("00");
    EXPECT_EQ(nf.first_value_, "00");
    EXPECT_EQ(nf.optional_value_, "00");
}

TEST(NumericFunctionTestEdge, AlphanumericValue) {
    NumericFunction nf("3");
    EXPECT_EQ(nf.bump("r3"), "r4");
    NumericFunction nf2("3");
    EXPECT_EQ(nf2.bump("r3-001"), "r4-001");
}

TEST(NumericFunctionTestEdge, InvalidFirstValueThrows) {
    EXPECT_THROW(NumericFunction("abc"), std::invalid_argument);
}

TEST(NumericFunctionTestEdge, NoDigitsThrows) {
    NumericFunction n;
    EXPECT_THROW(n.bump("abc"), std::invalid_argument);
}

TEST(ValuesFunctionTestEdge, BumpAndErrors) {
    ValuesFunction vf({ "alpha", "beta", "rc", "final" });
    EXPECT_EQ(vf.bump("alpha"), "beta");
    EXPECT_EQ(vf.bump("beta"), "rc");
    EXPECT_EQ(vf.bump("rc"), "final");
    EXPECT_THROW(vf.bump("final"), std::invalid_argument);
}

TEST(ValuesFunctionTestEdge, InitInvalidEmpty) {
    EXPECT_THROW(ValuesFunction({}), std::invalid_argument);
}

TEST(ValuesFunctionTestEdge, OptionalValueNotInValuesThrows) {
    EXPECT_THROW(ValuesFunction({"a", "b"}, "c"), std::invalid_argument);
}

TEST(ValuesFunctionTestEdge, FirstValueNotInValuesThrows) {
    EXPECT_THROW(ValuesFunction({"a", "b"}, "", "c"), std::invalid_argument);
}