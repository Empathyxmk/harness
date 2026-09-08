#include <gtest/gtest.h>
#include "itsdangerous_module_version.h"
#include <string>

// Test __version__ property / deprecation handling (simulate as best as possible in C++).
TEST(InitTest, VersionIsString) {
    std::string version = itsdangerous_get_version();
    EXPECT_FALSE(version.empty());
    EXPECT_NE(version.find('.'), std::string::npos);
    // Simulation: Can't check for deprecation warnings, but check the getter works.
}

TEST(InitTest, ImportlibVersion) {
    std::string v = itsdangerous_get_version(); // In C++, simulate as above.
    EXPECT_FALSE(v.empty());
    EXPECT_NE(v.find('.'), std::string::npos);
}