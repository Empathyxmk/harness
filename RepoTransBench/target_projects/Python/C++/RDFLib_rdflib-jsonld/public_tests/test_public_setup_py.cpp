#include <gtest/gtest.h>
#include <fstream>
#include <string>
#include <cstdlib>

std::string getSetupPyPath() {
    // Assume setup.py in project root
    return std::string("setup.py");
}

// Test that running setup.py with fake arg produces nonzero exit code and some output
TEST(PublicSetupPy, SetupRunsWithFakeArgReturnsError) {
    std::string command = "python " + getSetupPyPath() + " --foobar123 > setup_py_fake_output.txt 2>&1";
    int ret = std::system(command.c_str());
    // Should exit with error (non-0) and have output
    std::ifstream ifs("setup_py_fake_output.txt");
    std::string out;
    bool has_output = false;
    if (ifs.is_open()) {
        std::string line;
        while (std::getline(ifs, line)) {
            if (!line.empty()) {
                has_output = true;
                break;
            }
        }
        ifs.close();
        std::remove("setup_py_fake_output.txt");
    }
    EXPECT_NE(ret, 0);
    EXPECT_TRUE(has_output);
}

TEST(PublicSetupPy, SetupPyFileExistsAndHasCode) {
    std::ifstream ifs(getSetupPyPath());
    ASSERT_TRUE(ifs.good());
    std::string contents((std::istreambuf_iterator<char>(ifs)), std::istreambuf_iterator<char>());
    EXPECT_TRUE(contents.find("setup(") != std::string::npos ||
                contents.find("def ") != std::string::npos ||
                contents.find("import ") != std::string::npos ||
                contents.find("class ") != std::string::npos);
}