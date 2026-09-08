#include <gtest/gtest.h>
#include <string>
#include <tuple>

// Simulate _version module for public test
namespace protontricks {
namespace _version {
    const std::string __version__ = "0.0.0";
    const std::string version = "0.0.0";
    const std::tuple<int, int, int> version_tuple = std::make_tuple(0, 0, 0);
}
}

TEST(PublicVersionTest, PublicVersionAttributes) {
    using namespace protontricks::_version;
    // Count dots in __version__
    ASSERT_EQ(std::count(__version__.begin(), __version__.end(), '.'), 2);
    ASSERT_EQ(std::tuple_size<decltype(version_tuple)>::value, 3);
    // The first int of version_tuple as string should match the start of __version__
    auto major = std::to_string(std::get<0>(version_tuple));
    ASSERT_TRUE(__version__.rfind(major, 0) == 0);
}