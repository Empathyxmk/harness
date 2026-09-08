#include "gtest/gtest.h"
#include "sample/init.h"
#include <sstream>
#include <iostream>
#include <string>

TEST(InitTests, MainPrintsMessage) {
    // Redirect std::cout to a string
    std::stringstream buffer;
    std::streambuf* old = std::cout.rdbuf(buffer.rdbuf());

    sample::init::main();
    
    std::cout.rdbuf(old);
    std::string output = buffer.str();
    EXPECT_NE(output.find("Call your main application code here"), std::string::npos);
}