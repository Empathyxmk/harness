#include <gtest/gtest.h>
#include <fstream>
#include <string>
#include <filesystem>

TEST(PublicSetupPyTest, VersionExists) {
    namespace fs = std::filesystem;
    std::string setup_path = "setup.py";
    ASSERT_TRUE(fs::exists(setup_path));
    std::ifstream infile(setup_path);
    ASSERT_TRUE(infile.is_open());
    std::string content((std::istreambuf_iterator<char>(infile)), std::istreambuf_iterator<char>());
    ASSERT_NE(content.find("version"), std::string::npos);
}

TEST(PublicSetupPyTest, DescriptionExists) {
    namespace fs = std::filesystem;
    std::string setup_path = "setup.py";
    ASSERT_TRUE(fs::exists(setup_path));
    std::ifstream infile(setup_path);
    ASSERT_TRUE(infile.is_open());
    std::string content((std::istreambuf_iterator<char>(infile)), std::istreambuf_iterator<char>());
    ASSERT_NE(content.find("description"), std::string::npos);
}