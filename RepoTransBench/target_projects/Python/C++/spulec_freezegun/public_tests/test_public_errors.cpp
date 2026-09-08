#include <gtest/gtest.h>
#include <string>

TEST(PublicErrorsTest, RaisesTypeError) {
    try {
        std::string s = "notanumber";
        std::stoi(s);
        FAIL();
    } catch (const std::invalid_argument&) {
        SUCCEED();
    }
}

TEST(PublicErrorsTest, RaisesValueError) {
    try {
        std::string f = "NaNnot";
        std::stof(f);
        FAIL();
    } catch (const std::invalid_argument&) {
        SUCCEED();
    }
}