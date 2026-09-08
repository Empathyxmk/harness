#include <gtest/gtest.h>
#include "pyzbar/scripts/read_zbar.h"
#include <vector>
#include <string>

TEST(ScriptsReadZbarPublic, CreateArgparserAndHelp) {
    auto parser = create_argparser();
    auto opts = parser.get_option_names();
    EXPECT_NE(std::find(opts.begin(), opts.end(), "quiet"), opts.end());
    EXPECT_NE(std::find(opts.begin(), opts.end(), "file"), opts.end());
}

TEST(ScriptsReadZbarPublic, HelpOption) {
    auto parser = create_argparser();
    std::string helptext = parser.format_help();
    std::string help_lower = helptext;
    std::transform(help_lower.begin(), help_lower.end(), help_lower.begin(), ::tolower);
    EXPECT_NE(help_lower.find("usage"), std::string::npos);
}