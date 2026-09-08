#include <gtest/gtest.h>
#include <string>
#include <sstream>
#include "../../src/rajinipp_apis.h"
#include "../test_helpers.h"

TEST(FlowControlTest, IfConditional) {
    std::stringstream output;
    rpp_exec_from_file("examples/if_conditional.rpp", output);
    std::string out = output.str();
    EXPECT_NE(out.find("x ( 15.0 ) is equal to 15!"), std::string::npos);
}

TEST(FlowControlTest, IfElse) {
    std::stringstream output;
    rpp_exec_from_file("examples/if_else_conditional.rpp", output);
    std::string out = output.str();
    EXPECT_NE(out.find("x ( 5.0 ) is less than 10!"), std::string::npos);
}

TEST(FlowControlTest, ForLoop) {
    std::stringstream output;
    rpp_exec_from_file("examples/for_loop.rpp", output);
    std::string out = output.str();
    EXPECT_NE(out.find("After loop: X = 14.0"), std::string::npos);
}

TEST(FlowControlTest, WhileLoop) {
    std::stringstream output;
    rpp_exec_from_file("examples/while_loop.rpp", output);
    std::string out = output.str();
    EXPECT_NE(out.find("breaking out of loop..."), std::string::npos);
}