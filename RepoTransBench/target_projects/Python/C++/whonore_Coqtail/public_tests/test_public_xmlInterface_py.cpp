#include <gtest/gtest.h>
#include <vector>
#include <string>

// Dummy flatten logic for XML public test
void flatten(const std::vector<std::string>& in, std::vector<std::string>& out) {
    for (const auto& s : in) out.push_back(s);
}

TEST(PublicXmlInterfacePyTest, PublicFlatten) {
    std::vector<std::string> in = {"a", "b"};
    std::vector<std::string> out;
    flatten(in, out);
    ASSERT_EQ(out.size(), 2);
    EXPECT_EQ(out[0], "a");
    EXPECT_EQ(out[1], "b");
}