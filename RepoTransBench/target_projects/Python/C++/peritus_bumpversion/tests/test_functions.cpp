#include <gtest/gtest.h>
#include "functions.h"

TEST(NumericFunctionTest, InitWithoutFirstValue) {
    NumericFunction func;
    EXPECT_EQ(func.first_value_, "0");
}

TEST(NumericFunctionTest, InitWithFirstValue) {
    NumericFunction func("5");
    EXPECT_EQ(func.first_value_, "5");
}

TEST(NumericFunctionTest, InitNonNumericFirstValue) {
    EXPECT_THROW(NumericFunction("a"), std::invalid_argument);
}

TEST(NumericFunctionTest, BumpSimpleNumber) {
    NumericFunction func;
    EXPECT_EQ(func.bump("0"), "1");
}

TEST(NumericFunctionTest, BumpPrefixAndSuffix) {
    NumericFunction func;
    EXPECT_EQ(func.bump("v0b"), "v1b");
}

TEST(ValuesFunctionTest, InitSimple) {
    ValuesFunction func({ "0", "1", "2" });
    EXPECT_EQ(func.optional_value_, "0");
    EXPECT_EQ(func.first_value_, "0");
}

TEST(ValuesFunctionTest, InitWithCorrectOptionalValue) {
    ValuesFunction func({ "0", "1", "2" }, "1");
    EXPECT_EQ(func.optional_value_, "1");
    EXPECT_EQ(func.first_value_, "0");
}

TEST(ValuesFunctionTest, InitWithCorrectFirstValue) {
    ValuesFunction func({ "0", "1", "2" }, "", "1");
    EXPECT_EQ(func.optional_value_, "0");
    EXPECT_EQ(func.first_value_, "1");
}

TEST(ValuesFunctionTest, InitWithCorrectOptionalAndFirstValue) {
    ValuesFunction func({ "0", "1", "2" }, "0", "1");
    EXPECT_EQ(func.optional_value_, "0");
    EXPECT_EQ(func.first_value_, "1");
}

TEST(ValuesFunctionTest, InitWithEmptyValues) {
    EXPECT_THROW(ValuesFunction({}), std::invalid_argument);
}

TEST(ValuesFunctionTest, InitWithIncorrectOptionalValue) {
    EXPECT_THROW(ValuesFunction({ "0", "1", "2" }, "3"), std::invalid_argument);
}

TEST(ValuesFunctionTest, InitWithIncorrectFirstValue) {
    EXPECT_THROW(ValuesFunction({ "0", "1", "2" }, "", "3"), std::invalid_argument);
}

TEST(ValuesFunctionTest, BumpValidValue) {
    ValuesFunction func({ "0", "5", "10" });
    EXPECT_EQ(func.bump("0"), "5");
}

TEST(ValuesFunctionTest, BumpAtEndThrows) {
    ValuesFunction func({ "0", "5", "10" });
    EXPECT_THROW(func.bump("10"), std::invalid_argument);
}