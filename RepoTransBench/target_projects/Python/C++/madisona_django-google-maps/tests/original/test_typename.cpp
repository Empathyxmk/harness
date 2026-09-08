#include <gtest/gtest.h>
#include <string>
#include "lib/typename_utils.h"

class X {};

TEST(TypeNameTests, SimpleTypeReturnsTypeNameAsString) {
    std::string s = "x";
    EXPECT_EQ("str", typename_func(s));
}
TEST(TypeNameTests, ClassObject) {
    X obj;
    EXPECT_EQ("type", typename_func(obj));
}