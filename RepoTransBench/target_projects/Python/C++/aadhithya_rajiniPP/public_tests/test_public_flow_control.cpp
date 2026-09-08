#include <gtest/gtest.h>
#include <string>
#include <sstream>
#include "../src/rajinipp_apis.h"

TEST(PublicFlowControlTest, IfStatementTrueBranch) {
    std::string code = R"(
    val x = 6
    if (x % 2 == 0) {
        print "even-case!";
    }
    )";
    std::stringstream output;
    rpp_exec(code, output);
    std::string out = output.str();
    EXPECT_NE(out.find("even-case!"), std::string::npos);
}

TEST(PublicFlowControlTest, WhileLoopPrint) {
    std::string code = R"(
    val count = 0
    while (count < 2) {
        print "loop: " + count;
        count = count + 1;
    }
    )";
    std::stringstream output;
    rpp_exec(code, output);
    std::string out = output.str();
    EXPECT_NE(out.find("loop: 0"), std::string::npos);
    EXPECT_NE(out.find("loop: 1"), std::string::npos);
}