#include <gtest/gtest.h>
#include "pyzbar/scripts/read_zbar.h"
#include <string>
#include <algorithm>

// The two tests cover argument handling and description printing

TEST(ScriptsReadZbar, MainHelp) {
    // Simulate argument handling: --help
    std::string output;
    EXPECT_THROW({
        output = read_zbar_main_with_args({"read_zbar.py", "--help"});
    }, std::runtime_error);
    // Output must contain "usage" or "Usage"
    EXPECT_TRUE(output.find("usage") != std::string::npos || output.find("Usage") != std::string::npos);
}

TEST(ScriptsReadZbar, MainNoArgs) {
    std::string output;
    EXPECT_THROW({
        output = read_zbar_main_with_args({"read_zbar.py"});
    }, std::runtime_error);
    std::string output_lower = output;
    std::transform(output_lower.begin(), output_lower.end(), output_lower.begin(), ::tolower);
    EXPECT_TRUE(output_lower.find("usage") != std::string::npos || output_lower.find("error") != std::string::npos || !output.empty());
}