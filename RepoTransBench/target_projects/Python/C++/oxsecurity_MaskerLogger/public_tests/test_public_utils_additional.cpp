#include <gtest/gtest.h>
#include <string>
#include "../src/utils.h"

using maskerlogger::get_config_file_path;

TEST(TestUtilsAdditionalPublic, GetConfigFilePathOtherCustom) {
    std::string cfg = get_config_file_path("anotherpublic.toml");
    ASSERT_GE(cfg.size(), strlen("anotherpublic.toml"));
    ASSERT_EQ(cfg.rfind("anotherpublic.toml"), cfg.size() - strlen("anotherpublic.toml"));
}

TEST(TestUtilsAdditionalPublic, GetConfigFilePathFolderCheck) {
    std::string cfg = get_config_file_path();
    // Split by "/" or "\\"
    bool found = false;
    size_t pos = 0;
    while (true) {
        size_t next = cfg.find('/', pos);
        std::string part = cfg.substr(pos, next-pos);
        if (part == "config") { found = true; break; }
        if (next == std::string::npos) break;
        pos = next+1;
    }
    size_t bk = cfg.find('\\');
    if (!found && bk != std::string::npos) {
        // Try backslash
        pos = 0;
        while (true) {
            size_t next = cfg.find('\\', pos);
            std::string part = cfg.substr(pos, next-pos);
            if (part == "config") { found = true; break; }
            if (next == std::string::npos) break;
            pos = next+1;
        }
    }
    ASSERT_TRUE(found);
}