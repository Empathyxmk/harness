#include <gtest/gtest.h>
#include "itsdangerous_module_version.h"
#include <string>

TEST(InitPublicTest, VersionIsStringPublic) {
    std::string version = itsdangerous_get_version();
    EXPECT_FALSE(version.empty());
    EXPECT_NE(version.find('.'), std::string::npos);
}

TEST(InitPublicTest, ImportlibVersionPublic) {
    std::string v = itsdangerous_get_version();
    EXPECT_FALSE(v.empty());
    EXPECT_GE(std::count(v.begin(), v.end(), '.'), 1);
}