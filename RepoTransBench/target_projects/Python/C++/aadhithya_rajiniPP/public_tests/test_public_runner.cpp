#include <gtest/gtest.h>
#include <string>
#include <sstream>
#include "../src/rajinipp_runner.h"

TEST(PublicRunnerTest, TokenizeAndExec) {
    RppRunner runner;
    std::stringstream output;
    runner.exec("print 1234;", output);
    std::string out = output.str();
    EXPECT_NE(out.find("1234"), std::string::npos);
}

TEST(PublicRunnerTest, EvalSimpleLine) {
    RppRunner runner;
    double result = runner.eval("10 + 50");
    EXPECT_TRUE(result == 60.0 || result == 60);
}