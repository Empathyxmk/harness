#include <gtest/gtest.h>
#include "showme/core.h"
#include <vector>
#include <string>
#include <sstream>
#include <iostream>

namespace {

// Simulate setup.py monkeypatch/argv tests via calling the C++ equivalent
TEST(SetupPy, PublishBranchSimulation) {
    std::vector<std::string> argv = {"setup.py", "publish"};
    std::stringstream outbuf;
    std::streambuf* cout_save = std::cout.rdbuf(outbuf.rdbuf());

    showme::core::setup_py_main(argv);

    std::cout.rdbuf(cout_save);

    std::string output = outbuf.str();
    EXPECT_NE(output.find("setup_py_main called with"), std::string::npos);
    EXPECT_NE(output.find("publish"), std::string::npos);
}

TEST(SetupPy, SetupRunsSimulation) {
    std::vector<std::string> argv = {"setup.py", "install"};
    std::stringstream outbuf;
    std::streambuf* cout_save = std::cout.rdbuf(outbuf.rdbuf());

    showme::core::setup_py_main(argv);

    std::cout.rdbuf(cout_save);

    std::string output = outbuf.str();
    EXPECT_NE(output.find("setup_py_main called with"), std::string::npos);
    EXPECT_NE(output.find("install"), std::string::npos);
}

}