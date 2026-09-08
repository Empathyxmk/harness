#include <gtest/gtest.h>
#include <string>

TEST(PublicImportAliasTest, ImportAliasInt) {
    int x = std::stoi("456");
    ASSERT_EQ(x, 456);
}

TEST(PublicImportAliasTest, ImportAliasList) {
    std::vector<int> v{1,2,3};
    ASSERT_EQ(v[0], 1);
    ASSERT_EQ(v[1], 2);
    ASSERT_EQ(v[2], 3);
}