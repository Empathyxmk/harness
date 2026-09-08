#include <gtest/gtest.h>
#include <string>
#include <fstream>
#include <sstream>

TEST(DocsConfPy, DocsConfImport) {
    // Simulate opening and "executing" a docs conf file
    // We'll just check we can open/read docs/conf.py, and parse first line.
    std::string path = "docs/conf.py";
    std::ifstream conf(path);
    ASSERT_TRUE(conf.is_open());
    std::string first_line;
    std::getline(conf, first_line);
    EXPECT_FALSE(first_line.empty());
    // Can't exec python, but can simulate codepath
}