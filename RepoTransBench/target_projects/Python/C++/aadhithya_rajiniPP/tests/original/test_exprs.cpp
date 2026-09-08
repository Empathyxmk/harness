#include <gtest/gtest.h>
#include <string>
#include <sstream>
#include "../../src/rajinipp_apis.h"
#include "../test_helpers.h"

TEST(ExprsTest, ConditionalExprs) {
    std::stringstream output;
    rpp_exec_from_file("examples/if_conditional.rpp", output);
    std::string out = output.str();
    EXPECT_NE(out.find("x ( 15.0 ) is equal to 15!"), std::string::npos);
}

TEST(ExprsTest, LogicalExprs) {
    std::stringstream output;
    rpp_exec_from_file("examples/logical_ops.rpp", output);
    std::string out = output.str();
    EXPECT_NE(out.find("x != b:  True"), std::string::npos);
}

TEST(ExprsTest, MathExprs) {
    std::stringstream output;
    rpp_exec_from_file("examples/math_ops.rpp", output);
    std::string out = output.str();
    EXPECT_NE(out.find("modvar =  1.0"), std::string::npos);
}