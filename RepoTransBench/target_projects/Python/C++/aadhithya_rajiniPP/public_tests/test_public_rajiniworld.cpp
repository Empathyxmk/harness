#include <gtest/gtest.h>
#include "../src/rajinipp_rajiniworld.h"

TEST(PublicRajiniworldTest, VarsAndFunctionsDictNonempty) {
    auto& vars = rajinipp_rajiniworld::__vars__;
    auto& funcs = rajinipp_rajiniworld::__functions__;
    EXPECT_TRUE(vars.is_map());
    EXPECT_TRUE(funcs.is_map());
    EXPECT_TRUE(&vars != nullptr);
    EXPECT_TRUE(&funcs != nullptr);
}