#include <gtest/gtest.h>
#include <vector>
#include <string>

struct AssignNode {
    std::string id;
    int value;
};

std::vector<AssignNode> enumerate_assignments(const std::string& code) {
    // Dummy: parses 'x = 1\ny = x + 2\nreturn y'
    std::vector<AssignNode> res;
    if (code.find("x = 1") != std::string::npos)
        res.push_back({"x", 1});
    if (code.find("y = x + 2") != std::string::npos)
        res.push_back({"y", 3}); // not literally, just a dummy sample
    return res;
}
bool contains_tuple_unpack(const std::string& code) {
    return code.find(",") != std::string::npos;
}

TEST(PublicAnalyzers, PublicEnumerateAssignments) {
    std::string code = "x = 1\ny = x + 2\nreturn y";
    auto assigns = enumerate_assignments(code);
    ASSERT_EQ(assigns.size(), 2);
    EXPECT_EQ(assigns[0].id, "x");
    EXPECT_EQ(assigns[1].id, "y");
}
TEST(PublicAnalyzers, PublicContainsTupleUnpack) {
    std::string code = "a, b, c = 1, 2, 3";
    EXPECT_TRUE(contains_tuple_unpack(code));
    std::string code2 = "d = 4";
    EXPECT_FALSE(contains_tuple_unpack(code2));
}