#include <gtest/gtest.h>
#include <string>
#include <vector>
#include <sstream>

// Dummy XML splitter logic
std::vector<std::string> split_xml(const std::string& buf) {
    std::vector<std::string> res;
    std::string tmp;
    int depth = 0;
    for (char c : buf) {
        tmp += c;
        if (c == '<') depth++;
        if (c == '>') depth--;
        if (depth == 0 && !tmp.empty()) {
            res.push_back(tmp);
            tmp.clear();
        }
    }
    return res;
}

TEST(XmlInterfaceTest, SplitXmlSingleTag) {
    std::string input = "<coqtop/>";
    auto elems = split_xml(input);
    ASSERT_EQ(elems.size(), 1);
    EXPECT_EQ(elems[0], "<coqtop/>");
}

TEST(XmlInterfaceTest, SplitXmlMultipleTags) {
    std::string input = "<a></a><b></b>";
    auto elems = split_xml(input);
    ASSERT_EQ(elems.size(), 2);
    EXPECT_EQ(elems[0], "<a></a>");
    EXPECT_EQ(elems[1], "<b></b>");
}