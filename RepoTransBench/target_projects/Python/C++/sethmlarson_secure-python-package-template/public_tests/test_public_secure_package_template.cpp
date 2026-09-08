#include <gtest/gtest.h>
#include <string>
#include <sstream>
#include <vector>
#include <filesystem>
#include "secure_package_template/version.h"
#include "secure_package_template/pytyped.h"

namespace fs = std::filesystem;

// Helper to split a version string by '.'
static std::vector<std::string> splitVersion(const std::string& ver) {
    std::vector<std::string> parts;
    std::stringstream ss(ver);
    std::string item;
    while(std::getline(ss, item, '.')) {
        parts.push_back(item);
    }
    return parts;
}

// -- Test: Ensuring the package can be imported, __version__ is present, and format verification
TEST(PublicSecurePackageTemplateTests, PublicImportPackageAndVersion) {
    std::string version = secure_package_template::VersionModule::__version__();
    ASSERT_FALSE(version.empty());
    std::vector<std::string> parts = splitVersion(version);
    ASSERT_GE(parts.size(), 3u);
    for(const auto& p : parts) {
        for(char c : p) {
            ASSERT_TRUE(isdigit(c));
        }
    }
}

// -- Test: Direct module "_version" import match major.minor.patch pattern (dots == 2)
TEST(PublicSecurePackageTemplateTests, PublicDirectModuleImport) {
    std::string version = secure_package_template::VersionModule::__version__();
    ASSERT_EQ(std::count(version.begin(), version.end(), '.'), 2);
}

// -- Test: Existence of py.typed and correct stat usage
TEST(PublicSecurePackageTemplateTests, PublicPyTypedFileExists) {
    std::string path = secure_package_template::pytyped_file_path();
    try {
        auto stat = fs::status(path);
        ASSERT_TRUE(fs::exists(path));
        ASSERT_TRUE(fs::is_regular_file(path));
        ASSERT_GE(secure_package_template::pytyped_size(), 0u);
    } catch(const fs::filesystem_error&) {
        FAIL() << "py.typed file does not exist";
    }
}

// -- Test: "reload" and version type/length check
TEST(PublicSecurePackageTemplateTests, PublicReloadPreservesVersionAndType) {
    std::string version = secure_package_template::VersionModule::__version__();
    ASSERT_FALSE(version.empty());
    ASSERT_LT(version.length(), 20u);
}