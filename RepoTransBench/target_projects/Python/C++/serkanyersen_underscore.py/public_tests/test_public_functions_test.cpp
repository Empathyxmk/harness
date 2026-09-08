#include <gtest/gtest.h>
#include "underscore.h"
#include <string>
#include <vector>

using namespace underscore;

TEST(TestPublicFunctions, OncePublic) {
    std::vector<std::string> called;
    auto func = [&called](){ called.push_back("called"); return std::string("foo"); };
    auto once_func = once_str(func); // Use string-returning once for this test
    EXPECT_EQ(once_func(), "foo");
    once_func();
    std::vector<std::string> expected{"called"};
    EXPECT_EQ(called, expected);
}