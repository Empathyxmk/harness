#include <gtest/gtest.h>
#include <filesystem>
#include <fstream>

TEST(TestInitAndSetup, test_version) {
    std::ifstream version_file("include/haishoku/version.h");
    std::string version;
    if (version_file.is_open())
        getline(version_file, version);
    EXPECT_FALSE(version.empty());
    EXPECT_NE(version.find('.'), std::string::npos);
}

TEST(TestInitAndSetup, test_setup_callable) {
    std::filesystem::path setup = std::filesystem::current_path() / "CMakeLists.txt";
    EXPECT_TRUE(std::filesystem::exists(setup));
    // Simulate: has setup/packaging entry (CMakeLists.txt)
}

TEST(TestInitAndSetup, test_license_file) {
    EXPECT_TRUE(std::filesystem::exists("LICENSE"));
}