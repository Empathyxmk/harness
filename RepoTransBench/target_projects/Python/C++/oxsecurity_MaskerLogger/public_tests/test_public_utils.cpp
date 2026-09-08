#include <gtest/gtest.h>
#include <string>
#include "../src/utils.h"

using maskerlogger::get_config_file_path;

TEST(TestUtilsPublic, GetConfigFilePathNonDefault) {
    std::string path = get_config_file_path("alternative_config.toml");
    ASSERT_GE(path.size(), strlen("alternative_config.toml"));
    ASSERT_EQ(path.rfind("alternative_config.toml"), path.size() - strlen("alternative_config.toml"));
}

TEST(TestUtilsPublic, GetConfigFilePathContainsMaskerlogger) {
    std::string path = get_config_file_path();
    ASSERT_NE(path.find("maskerlogger"), std::string::npos);
}