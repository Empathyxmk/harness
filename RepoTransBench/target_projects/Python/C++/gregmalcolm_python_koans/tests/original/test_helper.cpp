#include "gtest/gtest.h"
#include "lib/helper.h"

TEST(TestHelper, ThatGetClassNameWorksWithAStringInstance) {
    EXPECT_EQ(std::string("str"), cls_name(std::string("hello")));
}

TEST(TestHelper, ThatGetClassNameWorksWithAnInt) {
    EXPECT_EQ(std::string("int"), cls_name(4));
}

TEST(TestHelper, ThatGetClassNameWorksWithATuple) {
    std::tuple<int, std::string, std::vector<int>> t = std::make_tuple(3, "pie", std::vector<int>());
    EXPECT_EQ(std::string("tuple"), cls_name(t));
}