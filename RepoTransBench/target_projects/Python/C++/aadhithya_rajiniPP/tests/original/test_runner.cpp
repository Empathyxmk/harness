#include <gtest/gtest.h>
#include <string>
#include <sstream>
#include "../../src/rajinipp_apis.h"
#include "../test_helpers.h"

TEST(RunnerTest, ExecHelloWorld) {
    std::stringstream output;
    rpp_exec_from_file("examples/hello_world.rpp", output);
    std::string out = output.str();
    EXPECT_EQ(out.find("Hello, World!"), 0);
}

TEST(RunnerTest, EvalSimpleExpr) {
    double out = rpp_eval_simple_expression("5+5;");
    EXPECT_EQ(out, 10.0);
}