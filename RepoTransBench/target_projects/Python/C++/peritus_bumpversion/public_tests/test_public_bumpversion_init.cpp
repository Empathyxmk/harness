#include <gtest/gtest.h>
#include "init.h"

TEST(PublicBumpversionInit, MainModuleImportablePublic) {
    EXPECT_EQ(get_description(), "Peritus BumpVersion tool");
}

TEST(PublicBumpversionInit, VersionPropertyExistencePublic) {
    std::string ver = get_version();
    EXPECT_FALSE(ver.empty());
}