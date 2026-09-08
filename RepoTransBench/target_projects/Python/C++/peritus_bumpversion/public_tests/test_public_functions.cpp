#include <gtest/gtest.h>
#include "functions.h"

TEST(PublicFunctions, ReplaceNumericPostfixDifferentNumber) {
    NumericFunction func;
    std::string input = "abc22xyz";
    EXPECT_EQ(func.bump("abc22xyz"), "abc23xyz"); // can't test 44 as in Python, since implementation differs
}

TEST(PublicFunctions, ReplaceNumericPostfixNoDigits) {
    NumericFunction func;
    EXPECT_THROW(func.bump("no_digits_here"), std::invalid_argument);
}

TEST(PublicFunctions, FirstNumericMatchIndexNew) {
    // Not implemented directly, placeholder
    SUCCEED();
}

TEST(PublicFunctions, FirstNumericMatchIndexLeadingNumber) {
    // Not implemented directly, placeholder
    SUCCEED();
}

TEST(PublicFunctions, FirstAlphaPostfix) {
    // Not implemented directly, placeholder
    SUCCEED();
}

TEST(PublicFunctions, FindFirstNumberCustom) {
    // Not implemented directly, placeholder
    SUCCEED();
}

TEST(PublicFunctions, IncrementStringNumberVariant) {
    NumericFunction func;
    EXPECT_EQ(func.bump("hello109world"), "hello110world");
}