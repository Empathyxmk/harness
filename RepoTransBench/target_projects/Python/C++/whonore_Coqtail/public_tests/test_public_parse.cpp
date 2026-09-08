#include <gtest/gtest.h>
#include <string>
#include <vector>
#include <sstream>

std::vector<std::string> split_colon(const std::string& line) {
    std::vector<std::string> res;
    std::stringstream ss(line);
    std::string item;
    while (std::getline(ss, item, ':'))
        res.push_back(item);
    return res;
}

TEST(PublicParseTest, PublicSplitColon) {
    auto parts = split_colon("A:B");
    ASSERT_EQ(parts.size(), 2);
    EXPECT_EQ(parts[0], "A");
    EXPECT_EQ(parts[1], "B");
}