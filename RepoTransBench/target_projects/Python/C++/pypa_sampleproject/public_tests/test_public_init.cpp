#include "gtest/gtest.h"
#include "sample/init.h"
#include <sstream>
#include <iostream>
#include <string>

TEST(PublicInitTests, MainPrintsCustomMessage) {
    // Like the public test: substring should match "main application code"
    std::stringstream buffer;
    std::streambuf* old = std::cout.rdbuf(buffer.rdbuf());

    sample::init::main();

    std::cout.rdbuf(old);
    std::string output = buffer.str();
    EXPECT_NE(output.find("main application code"), std::string::npos);
}