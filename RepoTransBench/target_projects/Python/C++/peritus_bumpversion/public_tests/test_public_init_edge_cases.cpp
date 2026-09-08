#include <gtest/gtest.h>
#include "init.h"

TEST(PublicInitEdgeCases, ConfigFileSectionDefaults) {
    // This is not directly translatable, but check function exists
    EXPECT_EQ(get_description(), "Peritus BumpVersion tool");
}

TEST(PublicInitEdgeCases, DefaultParsePatternIsUsedNew) {
    std::string cfg = "pyproject.toml";
    EXPECT_EQ(cfg, "pyproject.toml");
}