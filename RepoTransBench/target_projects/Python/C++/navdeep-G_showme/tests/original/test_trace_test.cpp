#include <gtest/gtest.h>
#include "showme/decorators.h"
#include <sstream>
#include <string>
#include <iostream>

namespace {

TEST(DecoratorTrace, OutputsTraceString) {
    auto fname = [](const std::string& a, const std::string& b) { return 0; };

    std::stringstream outbuf;
    std::streambuf* cout_save = std::cout.rdbuf(outbuf.rdbuf());

    // Simulate trace decorator output
    showme::decorators::trace_wrapper("fname", fname, "navdeep", "gill");
    std::cout.rdbuf(cout_save);

    std::string output = outbuf.str();
    EXPECT_NE(output.find("Calling fname"), std::string::npos);
    EXPECT_NE(output.find("navdeep"), std::string::npos);
    EXPECT_NE(output.find("gill"), std::string::npos);
}

}