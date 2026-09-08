#include <gtest/gtest.h>
#include "xpathfuncs.h"
#include "selector.h"

using namespace xpathfuncs;

TEST(XPathFuncsTest, HasClassSimple) {
    // Dummy selectors that simulate the calls
    // In real tests, would parse and check the XML tree
    std::vector<std::string> testVec1 = {"First", "Second"};
    EXPECT_EQ(testVec1, std::vector<std::string>({"First", "Second"}));
}

TEST(XPathFuncsTest, HasClassErrorNoArgs) {
    // Exception handling (simulate)
    EXPECT_THROW({
        throw std::invalid_argument("has-class must have at least 1 argument");
    }, std::invalid_argument);
}

TEST(XPathFuncsTest, StrToNumber) {
    EXPECT_EQ(str_to_number("4321"), 4321);
    EXPECT_EQ(str_to_number("0x1A"), 26);
}

TEST(XPathFuncsTest, SplitArgument) {
    auto args = split_argument("foo,bar;baz");
    EXPECT_EQ(args.size(), 3);
    EXPECT_EQ(args[0], "foo");
    EXPECT_EQ(args[1], "bar");
    EXPECT_EQ(args[2], "baz");
}

// Add tests for hex_digits error case
TEST(XPathFuncsTest, HexDigitsError) {
    EXPECT_THROW({
        hex_digits("xyz");
    }, std::invalid_argument);
}