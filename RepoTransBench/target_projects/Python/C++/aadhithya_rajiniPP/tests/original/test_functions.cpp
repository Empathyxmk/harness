#include <gtest/gtest.h>
#include <string>
#include <sstream>
#include "../../src/rajinipp_apis.h"
#include "../test_helpers.h"

TEST(FunctionsTest, Function) {
    std::stringstream output;
    rpp_exec_from_file("examples/functions_no_args.rpp", output);
    std::string out = output.str();
    EXPECT_NE(out.find("Hello from myfunc_one!"), std::string::npos);
}

TEST(FunctionsTest, FunctionReturn) {
    std::stringstream output;
    rpp_exec_from_file("examples/function_return.rpp", output);
    std::string out = output.str();
    EXPECT_NE(out.find("Value returned from myfunc_one: 100.0"), std::string::npos);
}