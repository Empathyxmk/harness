#include <gtest/gtest.h>
#include "init.h"

TEST(ModuleEdge, MinimalExports) {
    // Check that DESCRIPTION ("get_description") exists
    EXPECT_EQ(get_description(), "Peritus BumpVersion tool");
}