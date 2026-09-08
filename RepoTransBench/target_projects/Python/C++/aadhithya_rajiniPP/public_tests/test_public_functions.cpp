#include <gtest/gtest.h>
#include <string>
#include <sstream>
#include "../src/rajinipp_apis.h"

TEST(PublicFunctionsTest, FunctionDifferentContent) {
    std::string code = R"(
    function greet() {
      print "Public Test Hello!";
    }
    greet()
    )";
    std::stringstream output;
    rpp_exec(code, output);
    std::string out = output.str();
    EXPECT_NE(out.find("Public Test Hello!"), std::string::npos);
}

TEST(PublicFunctionsTest, FunctionReturnDifferentValue) {
    std::string code = R"(
    function add(a, b) {
      return a + b;
    }
    val result = add(75, 125)
    print "Public Test - Result: " + result;
    )";
    std::stringstream output;
    rpp_exec(code, output);
    std::string out = output.str();
    EXPECT_TRUE(
        out.find("Public Test - Result: 200") != std::string::npos ||
        out.find("Public Test - Result: 200.0") != std::string::npos
    );
}