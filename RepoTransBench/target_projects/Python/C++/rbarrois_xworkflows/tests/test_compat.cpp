#include <gtest/gtest.h>
#include <string>
#include "xworkflows/compat.h"
#include "xworkflows/base.h"

TEST(CompatTest, ImportCompatDirectSrc) {
    using namespace xworkflows::compat;
    // u() returns string as-is
    EXPECT_EQ(u("abc"), std::string("abc"));
    // is_string returns true for std::string
    EXPECT_TRUE(is_string("test"));
    EXPECT_FALSE(is_string(123));
    EXPECT_FALSE(is_string(nullptr));
}

TEST(CompatTest, ImportCompatFromSrcDirect) {
    // For C++ just include header again and check functions
    using namespace xworkflows::compat;
    EXPECT_EQ(u("def"), std::string("def"));
    EXPECT_TRUE(is_string("abc"));
    EXPECT_FALSE(is_string(std::vector<int>{}));
}

TEST(CompatTest, Python2ModeEquivalence) {
    // Simulates Python 2/3 str/unicode split. In C++ we check std::string, not bytes types.
    using namespace xworkflows::compat;
    std::string s("hey");
    EXPECT_TRUE(is_string(s));
    // Simulate bytes: in C++ that's std::vector<char> or const char*.
    const char *bytes = "bytes";
    EXPECT_FALSE(is_string(bytes));
}