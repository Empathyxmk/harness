#include <gtest/gtest.h>
#include <string>
#include <sstream>
#include <vector>

// Simulates parsing a goal line in Coq output, splitting by colon
std::vector<std::string> split_colon(const std::string& line) {
    std::vector<std::string> res;
    std::stringstream ss(line);
    std::string item;
    while (std::getline(ss, item, ':'))
        res.push_back(item);
    return res;
}

TEST(ParseTest, SplitColonSimple) {
    std::string line = "foo:bar:baz";
    auto parts = split_colon(line);
    ASSERT_EQ(parts.size(), 3);
    EXPECT_EQ(parts[0], "foo");
    EXPECT_EQ(parts[1], "bar");
    EXPECT_EQ(parts[2], "baz");
}

TEST(ParseTest, SplitColon_OneColon) {
    std::string line = "A:B";
    auto parts = split_colon(line);
    ASSERT_EQ(parts.size(), 2);
    EXPECT_EQ(parts[0], "A");
    EXPECT_EQ(parts[1], "B");
}

TEST(ParseTest, NoColon) {
    std::string line = "NoColonsHere";
    auto parts = split_colon(line);
    ASSERT_EQ(parts.size(), 1);
    EXPECT_EQ(parts[0], "NoColonsHere");
}