#include <gtest/gtest.h>
#include <cstdlib>
#include <string>
#include <fstream>
#include <sstream>

// C++ doesn't have 'import setup.py'. 
// We simulate: See if the setup file exists and is readable.

TEST(SetupTest, SetupInvokesSetuptools) {
    std::ifstream f("setup.py");
    ASSERT_TRUE(f.is_open()) << "Unable to open setup.py";
    // Additionally, we can check it contains "setuptools" as a very loose parse
    std::stringstream buffer;
    buffer << f.rdbuf();
    ASSERT_TRUE(buffer.str().find("setuptools") != std::string::npos);
}