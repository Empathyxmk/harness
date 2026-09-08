#include <gtest/gtest.h>
#include <string>

std::string get_public_version() {
    return "1.2.3";
}

TEST(TestPublicVersion, PublicVersionString) {
    auto version_str = get_public_version();
    EXPECT_TRUE(version_str.find('.') != std::string::npos);
    int dot_count = 0;
    for (char c : version_str) if (c == '.') dot_count++;
    EXPECT_EQ(dot_count, 2);
}