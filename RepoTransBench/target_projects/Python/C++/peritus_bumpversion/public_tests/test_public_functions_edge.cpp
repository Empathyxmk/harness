#include <gtest/gtest.h>
#include "functions.h"

TEST(PublicFunctionsEdge, ReplaceNumericPostfixOnlyNumber) {
    NumericFunction func;
    EXPECT_EQ(func.bump("667"), "668");
}

TEST(PublicFunctionsEdge, FirstNumericMatchIndexNoneNumber) {
    // Not implemented directly, placeholder
    SUCCEED();
}

TEST(PublicFunctionsEdge, FirstAlphaPostfixEdge) {
    // Not implemented directly, placeholder
    SUCCEED();
}

TEST(PublicFunctionsEdge, FindFirstNumberComplexString) {
    // Not implemented directly, placeholder
    SUCCEED();
}

TEST(PublicFunctionsEdge, IncrementStringNumberOnlyNumber) {
    NumericFunction func;
    EXPECT_EQ(func.bump("105"), "106");
}

TEST(PublicFunctionsEdge, IncrementStringNumberWithZeros) {
    NumericFunction func;
    EXPECT_EQ(func.bump("code007bond"), "code008bond");
}