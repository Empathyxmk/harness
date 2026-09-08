#include <gtest/gtest.h>
#include <fstream>
#include <string>

TEST(SetupPyTest, SetupFileExists) {
    std::ifstream setup("setup.py");
    ASSERT_TRUE(setup.good()) << "setup.py should exist in the project root";
}

TEST(SetupPyTest, SetupFileContainsVersion) {
    std::ifstream setup("setup.py");
    ASSERT_TRUE(setup.good()) << "setup.py should exist";
    std::string line;
    bool found_version = false;
    while (std::getline(setup, line)) {
        if (line.find("version") != std::string::npos) {
            found_version = true;
            break;
        }
    }
    ASSERT_TRUE(found_version) << "setup.py should contain version";
}