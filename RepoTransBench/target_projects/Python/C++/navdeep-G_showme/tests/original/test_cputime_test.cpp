#include <gtest/gtest.h>
#include "showme/decorators.h"
#include <cmath>
#include <sstream>
#include <iostream>

namespace {

TEST(DecoratorCpuTime, RunsFunctionAndPrintsCpuTime) {
    auto test = []() {
        for (int i = 0; i < 1000; ++i) {
            volatile double a = std::pow(i, i); // Side-effect to prevent optimizing
        }
        return 1;
    };

    std::stringstream outbuf;
    std::streambuf* cout_save = std::cout.rdbuf(outbuf.rdbuf());
    int result = showme::decorators::cputime_wrapper(test);
    std::cout.rdbuf(cout_save);

    std::string output = outbuf.str();
    EXPECT_NE(output.find("CPU time for"), std::string::npos);
    EXPECT_EQ(result, 1);
}

}