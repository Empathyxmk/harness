#include <gtest/gtest.h>
#include <string>
#include <sstream>
#include "../../src/rajinipp_apis.h"
#include "../test_helpers.h"

TEST(PrintTest, PrintHelloWorld) {
    std::stringstream output;
    rpp_exec_from_file("examples/hello_world.rpp", output);
    std::string out = output.str();
    EXPECT_EQ(out.substr(0, out.size()), "Hello, World!");
}

TEST(PrintTest, MultiPrint) {
    std::stringstream output;
    rpp_exec_from_file("examples/multi_print.rpp", output);
    std::string out = output.str();
    EXPECT_EQ(out.substr(0, out.size()), "5 + 5 = 10.0");
}