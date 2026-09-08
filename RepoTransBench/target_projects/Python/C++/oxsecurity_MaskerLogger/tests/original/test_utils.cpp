#include <gtest/gtest.h>
#include <string>
#include "../../src/utils.h"

TEST(TestUtils, GetConfigFilePath) {
    std::string path = maskerlogger::get_config_file_path();
    ASSERT_TRUE(path.size() >= 13);
    ASSERT_TRUE(path.rfind("gitleaks.toml") == path.size() - strlen("gitleaks.toml"));
    ASSERT_NE(path.find("config"), std::string::npos);
}

TEST(TestUtils, GetConfigFilePathCustom) {
    std::string cfg = maskerlogger::get_config_file_path("customfile.toml");
    ASSERT_TRUE(cfg.size() >= 15);
    ASSERT_TRUE(cfg.rfind("customfile.toml") == cfg.size() - strlen("customfile.toml"));
}