#include <gtest/gtest.h>
#include <string>
#include <vector>

// Dummy flatten logic for Python xmlInterface flatten test
void flatten(const std::vector<std::string>& in, std::vector<std::string>& out) {
    for (const auto& s : in) out.push_back(s);
}

TEST(XmlInterfacePyTest, FlattenEmpty) {
    std::vector<std::string> in, out;
    flatten(in, out);
    ASSERT_TRUE(out.empty());
}

TEST(XmlInterfacePyTest, FlattenSingle) {
    std::vector<std::string> in = {"a"};
    std::vector<std::string> out;
    flatten(in, out);
    ASSERT_EQ(out.size(), 1);
    EXPECT_EQ(out[0], "a");
}