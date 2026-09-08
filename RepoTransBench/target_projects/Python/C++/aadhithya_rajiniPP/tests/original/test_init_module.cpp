#include <gtest/gtest.h>
#include "../../src/rajinipp_module.h"

TEST(InitModuleTest, VersionAndStr) {
    // Test __version__ and __version_str__ existence and contents
    EXPECT_TRUE(rajinipp::__has_version());
    EXPECT_TRUE(rajinipp::__has_version_str());
    std::string vstr = rajinipp::__version_str();
    EXPECT_NE(vstr.find("rajini++"), std::string::npos);
    EXPECT_TRUE(rajinipp::__has_all());
}

TEST(InitModuleTest, RppRunnerImported) {
    // rpp should be an instance of runner::RppRunner
    EXPECT_TRUE(rajinipp::rpp_is_instance_of_rpprunner());
}