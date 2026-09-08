#include <gtest/gtest.h>
#include "showme/decorators.h"
#include <sstream>
#include <iostream>

namespace {

TEST(DecoratorDocs, PrintsDocstring) {
    auto test = []() { return 0; };

    std::stringstream outbuf;
    std::streambuf* cout_save = std::cout.rdbuf(outbuf.rdbuf());
    // Simulate docstring printing
    showme::decorators::docs_wrapper("sample docstring for test", test);
    std::cout.rdbuf(cout_save);

    std::string output = outbuf.str();
    // Look for docstring in output (as in doctest)
    EXPECT_NE(output.find("sample docstring for test"), std::string::npos);
}

}