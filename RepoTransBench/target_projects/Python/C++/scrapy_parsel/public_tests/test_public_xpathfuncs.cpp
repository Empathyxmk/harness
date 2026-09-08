#include <gtest/gtest.h>
#include "xpathfuncs.h"

using namespace xpathfuncs;

TEST(PublicXpathFuncs, TokenizeBasic) {
    auto tokens = tokenize(" foo-bar baz-qux ");
    ASSERT_EQ(tokens.size(), 2);
    EXPECT_EQ(tokens[0], "foo-bar");
    EXPECT_EQ(tokens[1], "baz-qux");
}

TEST(PublicXpathFuncs, TokenizeWithCommas) {
    auto tokens = tokenize("123, test, foo");
    ASSERT_EQ(tokens.size(), 3);
    EXPECT_EQ(tokens[0], "123,");
    EXPECT_EQ(tokens[1], "test,");
    EXPECT_EQ(tokens[2], "foo");
}

TEST(PublicXpathFuncs, StrToNumber) {
    EXPECT_EQ(str_to_number("4321"), 4321);
    EXPECT_EQ(str_to_number("0x1A"), 26);
}

TEST(PublicXpathFuncs, SplitArgument) {
    auto args = split_argument("foo,bar;baz");
    ASSERT_EQ(args.size(), 3);
    EXPECT_EQ(args[0], "foo");
    EXPECT_EQ(args[1], "bar");
    EXPECT_EQ(args[2], "baz");
}

TEST(PublicXpathFuncs, HexDigitsError) {
    EXPECT_THROW({
        hex_digits("xyz");
    }, std::invalid_argument);
}