#include <gtest/gtest.h>
#include <string>

namespace chainbreaker_version {
    const std::string __version__ = "1.2.3";
}

TEST(VersionTest, VersionIsString) {
    ASSERT_GE(chainbreaker_version::__version__.find("."), 0);
    ASSERT_GT(chainbreaker_version::__version__.size(), 0);
}