#include <gtest/gtest.h>
#include "showme/core.h"
#include <sstream>
#include <vector>
#include <string>
#include <iostream>

namespace {

TEST(PublicSetupPy, SetupPyMainRunsCallsPrint) {
    std::vector<std::string> argv = {"--version"};
    std::stringstream outbuf;
    std::streambuf* cout_save = std::cout.rdbuf(outbuf.rdbuf());
    showme::core::setup_py_main(argv);
    std::cout.rdbuf(cout_save);

    std::string output = outbuf.str();
    EXPECT_NE(output.find("setup_py_main called with"), std::string::npos);
    EXPECT_NE(output.find("--version"), std::string::npos);
}

}