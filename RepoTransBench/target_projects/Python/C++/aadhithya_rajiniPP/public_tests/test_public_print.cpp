#include <gtest/gtest.h>
#include <string>
#include <sstream>
#include "../src/rajinipp_apis.h"

TEST(PublicPrintTest, PrintSimpleMessage) {
    std::string code = "print \"Public output!\";";
    std::stringstream output;
    rpp_exec(code, output);
    std::string out = output.str();
    EXPECT_NE(out.find("Public output!"), std::string::npos);
}

TEST(PublicPrintTest, PrintNumberAndStringConcat) {
    std::string code = "val score = 99\nprint \"Score: \" + score;";
    std::stringstream output;
    rpp_exec(code, output);
    std::string out = output.str();
    EXPECT_NE(out.find("Score: 99"), std::string::npos);
}