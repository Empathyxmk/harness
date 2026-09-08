#include <gtest/gtest.h>
#include <string>

namespace chainbreaker_version {
    const std::string __version__ = "1.2.0";
    const char *__doc__ = "Version docstring";
}

TEST(PublicVersionTest, PublicVersionAttribute) {
    ASSERT_FALSE(chainbreaker_version::__version__.empty());
    auto v = chainbreaker_version::__version__;
    ASSERT_GT(v.find('.'), 0);
    auto count = std::count(v.begin(), v.end(), '.');
    ASSERT_GE(count, 1u);
}

TEST(PublicVersionTest, PublicVersionModuleDoc) {
    ASSERT_TRUE(chainbreaker_version::__doc__ != nullptr);
}