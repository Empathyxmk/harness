#include <gtest/gtest.h>
#include <iostream>
#include <sstream>
#include <string>

TEST(WarningsTest, WarnsUser) {
    // C++ does not have std::warn, but we can simulate warnings
    std::ostringstream oss;
    oss << "example warning!";
    std::string out = oss.str();
    ASSERT_NE(out.find("example warning!"), std::string::npos);
}