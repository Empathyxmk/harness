#include <gtest/gtest.h>
#include <string>
#include <sstream>

std::string parse_version(const std::string& text) {
    std::string prefix = "__version__ = '";
    auto idx = text.find(prefix);
    if (idx == std::string::npos) throw std::invalid_argument("No __version__ found");
    auto start = idx + prefix.size();
    auto end = text.find("'", start);
    return text.substr(start, end - start);
}

TEST(PublicCreateTagTest, ParseVersion) {
    std::string test = "__version__ = '2.8.9a-public'\n";
    ASSERT_EQ(parse_version(test), "2.8.9a-public");
}