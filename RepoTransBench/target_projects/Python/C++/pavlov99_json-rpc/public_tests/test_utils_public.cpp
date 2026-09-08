#include <gtest/gtest.h>
#include <jsonrpc/utils.h>
#include <string>

TEST(TestUtilsPublic, test_public_string) {
    std::string s = "public_string";
    EXPECT_TRUE(is_string(s)); // or other logic from test_utils_public.py
}

// (Add all other public test cases)