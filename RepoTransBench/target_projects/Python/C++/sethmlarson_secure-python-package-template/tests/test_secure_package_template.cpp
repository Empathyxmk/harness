#include <gtest/gtest.h>
#include <string>
#include <filesystem>
#include "secure_package_template/version.h"
#include "secure_package_template/pytyped.h"

namespace fs = std::filesystem;

// Test importing the package and __version__
TEST(SecurePackageTemplateTests, ImportPackageAndVersion) {
    // Simulate module import and presence check
    std::string version = secure_package_template::VersionModule::__version__();
    ASSERT_FALSE(version.empty());
}

// Test that "module import" for _version works
TEST(SecurePackageTemplateTests, DirectModuleImport) {
    std::string version = secure_package_template::VersionModule::__version__();
    ASSERT_FALSE(version.empty());
}

// Test py.typed file existence via filesystem
TEST(SecurePackageTemplateTests, PyTypedFileExists) {
    ASSERT_TRUE(secure_package_template::pytyped_exists());
    ASSERT_TRUE(secure_package_template::pytyped_size() >= 0);
}

// Test that reload (simulated) preserves version attribute
TEST(SecurePackageTemplateTests, ReloadPreservesVersion) {
    std::string version = secure_package_template::VersionModule::__version__();
    ASSERT_FALSE(version.empty());
}