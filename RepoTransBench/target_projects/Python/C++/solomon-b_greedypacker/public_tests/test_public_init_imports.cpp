#include <gtest/gtest.h>
#include "greedypacker/BinManager.h"
#include "greedypacker/Item.h"

TEST(PublicTestInitImports, Imports) {
    // Simulate "import greedypacker" and check API
    // Just test that the classes exist and are constructible
    greedypacker::BinManager bm(10, 5);
    greedypacker::Item it(2, 2);
    EXPECT_EQ(typeid(bm).name(), typeid(greedypacker::BinManager).name());
    EXPECT_EQ(typeid(it).name(), typeid(greedypacker::Item).name());
}