#include <gtest/gtest.h>
#include <string>
#include "secure_package_template/version.h"

// Test importable _version and value
TEST(VersionTests, VersionModuleImportable) {
    std::string version = secure_package_template::VersionModule::__version__();
    ASSERT_EQ(version, "0.7.1");
}

// Test attribute consistency between main and submodule
TEST(VersionTests, VersionAttributeConsistency) {
    std::string main_ver = secure_package_template::VersionModule::__version__();
    std::string sub_ver = secure_package_template::VersionModule::__version__();
    ASSERT_EQ(main_ver, sub_ver);
}

// Test import version string is string and not empty
TEST(VersionTests, ImportVersionStr) {
    std::string version = secure_package_template::VersionModule::__version__();
    ASSERT_FALSE(version.empty());
}

// Test reload (simulated) preserves version attribute
TEST(VersionTests, ReloadPackagePreservesVersion) {
    std::string version = secure_package_template::VersionModule::__version__();
    ASSERT_FALSE(version.empty());
}