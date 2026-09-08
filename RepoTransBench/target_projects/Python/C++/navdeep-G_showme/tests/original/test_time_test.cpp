#include <gtest/gtest.h>
#include "showme/decorators.h"
#include <cmath>
#include <sstream>
#include <iostream>

namespace {

TEST(DecoratorTime, RunsFunctionAndPrintsTime) {
    auto test = []() {
        for (int i = 0; i < 1000; ++i) {
            volatile double a = std::pow(i, i); // Force calculation (avoid optimization)
        }
        return 1;
    };

    std::stringstream outbuf;
    std::streambuf* cout_save = std::cout.rdbuf(outbuf.rdbuf());
    int result = showme::decorators::time_wrapper(test);
    std::cout.rdbuf(cout_save);

    std::string output = outbuf.str();
    EXPECT_NE(output.find("Execution speed of"), std::string::npos);
    EXPECT_EQ(result, 1);
}

}