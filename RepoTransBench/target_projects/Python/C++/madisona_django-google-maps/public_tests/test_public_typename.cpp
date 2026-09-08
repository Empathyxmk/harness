#include <gtest/gtest.h>
#include <string>
#include "lib/typename_utils.h"

class Y {};

TEST(TypeNamePublicTests, SimpleTypeReturnsTypeNameAsStringPublic) {
    std::string s = "abc";
    EXPECT_EQ("str", typename_func(s));
}
TEST(TypeNamePublicTests, ClassObjectPublic) {
    Y obj;
    EXPECT_EQ("type", typename_func(obj));
}