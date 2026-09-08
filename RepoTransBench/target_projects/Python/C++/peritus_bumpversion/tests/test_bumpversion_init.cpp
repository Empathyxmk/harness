#include <gtest/gtest.h>
#include "init.h"

TEST(PublicApi, IncludesDescription) {
    EXPECT_EQ(get_description(), "Peritus BumpVersion tool");
}

TEST(MainModule, Importable) {
    EXPECT_NO_THROW({
        // In C++ translation, if functions are available, that's sufficient
        (void)get_description();
        (void)get_version();
    });
}