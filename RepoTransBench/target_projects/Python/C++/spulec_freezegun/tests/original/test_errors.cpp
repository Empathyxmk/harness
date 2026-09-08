#include <gtest/gtest.h>
#include <stdexcept>
#include <string>

TEST(ErrorsTest, RaisesTypeError) {
    try {
        std::string s = "notanumber";
        std::stoi(s);
        FAIL();
    } catch (const std::invalid_argument&) {
        SUCCEED();
    }
}

TEST(ErrorsTest, RaisesValueError) {
    try {
        std::string f = "NaNnot";
        std::stof(f);
        FAIL();
    } catch (const std::invalid_argument&) {
        SUCCEED();
    }
}