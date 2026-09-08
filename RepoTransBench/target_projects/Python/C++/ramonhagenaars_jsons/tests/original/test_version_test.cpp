#include <gtest/gtest.h>
#include <string>
#include <vector>
#include <sstream>

std::string get_version() {
    // Example version: "1.2.3"
    return "1.2.3";
}

TEST(TestVersion, test_version) {
    std::string version = get_version();
    std::vector<std::string> split;
    std::stringstream ss(version);
    std::string part;
    while(std::getline(ss, part, '.')) {
        split.push_back(part);
    }
    EXPECT_EQ(split.size(), 3u);
}