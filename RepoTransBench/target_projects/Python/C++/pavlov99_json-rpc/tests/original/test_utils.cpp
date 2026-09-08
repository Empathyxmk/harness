#include <gtest/gtest.h>
#include <jsonrpc/utils.h>
#include <string>
#include <vector>

// Example stubs for illustration, mimic Python logic from test_utils.py

TEST(TestUtils, test_string_is_string) {
    std::string s = "hello";
    EXPECT_TRUE(is_string(s)); // is_string to be defined in jsonrpc/utils.h
}

TEST(TestUtils, test_is_string_on_int) {
    int x = 5;
    EXPECT_FALSE(is_string(x));
}

// (Add all other test cases from test_utils.py here, translating logic identically)