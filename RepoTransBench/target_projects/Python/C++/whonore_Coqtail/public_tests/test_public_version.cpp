#include <gtest/gtest.h>
#include <string>

// Extract version number if present
std::string parse_version(const std::string& raw) {
    auto v_pos = raw.find("version ");
    if (v_pos == std::string::npos) return "";
    auto start = v_pos + 8;
    auto end = raw.find(' ', start);
    if (end == std::string::npos) end = raw.size();
    return raw.substr(start, end - start);
}

TEST(PublicVersionTest, PublicParseVersion) {
    std::string input = "The Coq Proof Assistant, version 8.16.0 (October 2022)";
    EXPECT_EQ(parse_version(input), "8.16.0");
}