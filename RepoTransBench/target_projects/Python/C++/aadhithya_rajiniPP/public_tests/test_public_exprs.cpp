#include <gtest/gtest.h>
#include <string>
#include <sstream>
#include "../src/rajinipp_apis.h"

TEST(PublicExprsTest, SimpleArithmeticExpr) {
    std::string code = "print 20 + 10 + 5;";
    std::stringstream output;
    rpp_exec(code, output);
    std::string out = output.str();
    EXPECT_TRUE(out.find("35") != std::string::npos || out.find("35.0") != std::string::npos);
}

TEST(PublicExprsTest, FloatExprResult) {
    std::string code = "print 7.5 * 4;";
    std::stringstream output;
    rpp_exec(code, output);
    std::string out = output.str();
    EXPECT_TRUE(out.find("30") != std::string::npos || out.find("30.0") != std::string::npos);
}