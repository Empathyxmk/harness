#include <gtest/gtest.h>
#include "../src/rajinipp_module.h"

TEST(PublicInitModuleTest, VersionAndStr) {
    EXPECT_TRUE(rajinipp::__has_version());
    EXPECT_TRUE(rajinipp::__has_version_str());
    std::string vstr = rajinipp::__version_str();
    EXPECT_FALSE(vstr.empty());
    EXPECT_EQ(vstr.substr(0, 6), "rajini");
    EXPECT_TRUE(rajinipp::__has_all());
    std::vector<std::string> all = rajinipp::__all();
    EXPECT_FALSE(all.empty());
}

TEST(PublicInitModuleTest, RppRunnerImported) {
    EXPECT_EQ(rajinipp::rpp_type_name(), "RppRunner");
}