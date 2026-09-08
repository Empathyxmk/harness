#include <gtest/gtest.h>
#include "greedypacker/BinManager.h"
#include "greedypacker/Item.h"

TEST(TestPublicApi, BinManagerAndItem) {
    greedypacker::BinManager bm(15, 12);
    greedypacker::Item i1(7, 3);
    int bin_index = bm.insert(i1);
    EXPECT_EQ(bin_index, 0);
    EXPECT_GE(bm.getBin(0).width, i1.width);
    EXPECT_GE(bm.getBin(0).height, i1.height);
    EXPECT_TRUE(typeid(i1.x) == typeid(int));
    EXPECT_TRUE(typeid(i1.y) == typeid(int));
    EXPECT_TRUE(bm.hasInsertMethod());
}