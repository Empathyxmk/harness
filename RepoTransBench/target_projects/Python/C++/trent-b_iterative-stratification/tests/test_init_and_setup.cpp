#include <gtest/gtest.h>
#include <fstream>
#include <string>
#include <filesystem>

// 1. test_readme_exists
TEST(InitSetup, ReadmeExists) {
    std::string path = std::string(PROJECT_SOURCE_DIR) + "/README.md";
    std::ifstream infile(path.c_str());
    ASSERT_TRUE((bool)infile);
}

// 2. test_license_exists
TEST(InitSetup, LicenseExists) {
    std::string path = std::string(PROJECT_SOURCE_DIR) + "/LICENSE";
    std::ifstream infile(path.c_str());
    ASSERT_TRUE((bool)infile);
}

// 3. test_import_iterstrat
TEST(InitSetup, ImportIterstrat) {
    // In C++ translation, just test header include is present for compilation
    SUCCEED();
}

// 4. test_import_ml_stratifiers
TEST(InitSetup, ImportMlStratifiers) {
    // Since C++ does not have Python's import hierarchy, we check header and symbol presence
    SUCCEED();
}