#include <gtest/gtest.h>
#include <string>

TEST(InitPy, VersionString) {
    std::string __version__ = "1.2.3";
    EXPECT_TRUE(typeid(__version__) == typeid(std::string));
    size_t count = std::count(__version__.begin(), __version__.end(), '.');
    EXPECT_EQ(count, 2u);
}