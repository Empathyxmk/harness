#include <gtest/gtest.h>
#include "showme/decorators.h"
#include <sstream>
#include <string>
#include <iostream>

namespace {

TEST(PublicTrace, TraceFunctionalitySimulation) {
    auto trace_func = [](const std::string& msg, int number) { return 0; };

    std::stringstream outbuf;
    std::streambuf* cout_save = std::cout.rdbuf(outbuf.rdbuf());
    showme::decorators::trace_wrapper("trace_func", trace_func, "Trace public test", 456);
    std::cout.rdbuf(cout_save);

    std::string output = outbuf.str();
    EXPECT_NE(output.find("Trace public test"), std::string::npos);
    EXPECT_NE(output.find("456"), std::string::npos);
}

}