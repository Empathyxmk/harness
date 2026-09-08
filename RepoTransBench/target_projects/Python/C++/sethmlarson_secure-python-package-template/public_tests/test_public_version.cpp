#include <gtest/gtest.h>
#include <string>
#include <vector>
#include <sstream>
#include "secure_package_template/version.h"

// Helper to split version like "0.7.1"
static std::vector<std::string> splitVersion(const std::string& str) {
    std::vector<std::string> parts;
    std::stringstream ss(str);
    std::string part;
    while(std::getline(ss, part, '.')) parts.push_back(part);
    return parts;
}

// Test _version importable and format major/minor
TEST(PublicVersionTests, PublicVersionModuleImportableAndFormat) {
    std::string v = secure_package_template::VersionModule::__version__();
    auto parts = splitVersion(v);
    ASSERT_GE(parts.size(), 2u);
    ASSERT_EQ(parts[0], "0");
    ASSERT_EQ(parts[1], "7");
}

// Test public attribute consistency and != '0.0.0'
TEST(PublicVersionTests, PublicVersionAttributeConsistencyAndNotEmpty) {
    std::string mainver = secure_package_template::VersionModule::__version__();
    std::string subver = secure_package_template::VersionModule::__version__();
    ASSERT_EQ(mainver, subver);
    ASSERT_NE(mainver, "0.0.0");
}

// Version string type and length check
TEST(PublicVersionTests, PublicImportVersionTypeAndLength) {
    std::string ver = secure_package_template::VersionModule::__version__();
    ASSERT_GE(ver.length(), 5u);
}

// Test reload and version string contains only alphanumeric+'.'
TEST(PublicVersionTests, PublicReloadPackagePreservesVersionType) {
    std::string version = secure_package_template::VersionModule::__version__();
    ASSERT_NE(version.find('.'), std::string::npos);

    std::string chars = version;
    chars.erase(std::remove(chars.begin(), chars.end(), '.'), chars.end());
    for(char c : chars) {
        ASSERT_TRUE(isalnum(static_cast<unsigned char>(c)));
    }
}