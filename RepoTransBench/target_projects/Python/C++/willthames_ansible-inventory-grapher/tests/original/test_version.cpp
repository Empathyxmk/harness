#include <gtest/gtest.h>
#include <string>

std::string get_version() {
    return "1.2.3"; // Simulate: should be maintained as a string containing dots.
}

TEST(TestVersion, VersionString) {
    auto version_str = get_version();
    EXPECT_TRUE(version_str.find('.') != std::string::npos);
}