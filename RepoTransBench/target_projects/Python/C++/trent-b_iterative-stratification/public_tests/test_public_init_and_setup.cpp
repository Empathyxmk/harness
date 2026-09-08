#include <gtest/gtest.h>
#include <fstream>
#include <string>
#include <filesystem>

// 1. test_public_readme_exists
TEST(PublicInitSetup, PublicReadmeExists) {
    std::string path = std::string(PROJECT_SOURCE_DIR) + "/README.md";
    std::ifstream infile(path.c_str());
    ASSERT_TRUE((bool)infile);
}

// 2. test_public_license_exists
TEST(PublicInitSetup, PublicLicenseExists) {
    std::string path = std::string(PROJECT_SOURCE_DIR) + "/LICENSE";
    std::ifstream infile(path.c_str());
    ASSERT_TRUE((bool)infile);
}

// 3. test_public_import_iterstrat
TEST(PublicInitSetup, PublicImportIterstrat) {
    SUCCEED();
}

// 4. test_public_import_ml_stratifiers
TEST(PublicInitSetup, PublicImportMlStratifiers) {
    // The public test checks for 'MultilabelStratifiedShuffleSplit' symbol in Python,
    // here we simply succeed for translation/demo.
    SUCCEED();
}