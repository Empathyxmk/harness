#include <gtest/gtest.h>
#include <fstream>
#include <string>
#include <filesystem>

TEST(SetupPyTest, ExistsAndHasSetupCall) {
    namespace fs = std::filesystem;
    std::string setup_path = "setup.py";
    ASSERT_TRUE(fs::exists(setup_path));
    std::ifstream infile(setup_path);
    ASSERT_TRUE(infile.is_open());
    std::string content((std::istreambuf_iterator<char>(infile)), std::istreambuf_iterator<char>());
    infile.close();
    ASSERT_NE(content.find("setup("), std::string::npos);
    ASSERT_NE(content.find("__name__"), std::string::npos);
}