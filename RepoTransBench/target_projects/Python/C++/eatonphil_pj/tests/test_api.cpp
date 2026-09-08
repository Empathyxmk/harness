#include <gtest/gtest.h>
#include "pj.h"

TEST(PJAPI, ToStringDict) {
    pj::PjValue d = pj::PjValue::object({{"foo", pj::PjValue(1)}, {"bar", pj::PjValue(true)}});
    std::string s = pj::to_string(d);
    // Allow both key orders for dict string
    bool match = (s == "{\"foo\": 1, \"bar\": true}" || s == "{\"bar\": true, \"foo\": 1}");
    EXPECT_TRUE(match);
    // Round-trip
    pj::PjValue r = pj::from_string(s);
    EXPECT_EQ(r, d);
}

TEST(PJAPI, ToStringList) {
    pj::PjValue arr = pj::PjValue::array({pj::PjValue(1), pj::PjValue(2), pj::PjValue("abc")});
    std::string s = pj::to_string(arr);
    EXPECT_EQ(s, "[1, 2, \"abc\"]");
    std::string input = "{\"a\": " + s + "}";
    pj::PjValue r = pj::from_string(input);
    pj::PjValue expected = pj::PjValue::object({{"a", arr}});
    EXPECT_EQ(r, expected);
}

TEST(PJAPI, ToStringStr) {
    EXPECT_EQ(pj::to_string(pj::PjValue("abc")), "\"abc\"");
}

TEST(PJAPI, ToStringBool) {
    EXPECT_EQ(pj::to_string(pj::PjValue(true)), "true");
    EXPECT_EQ(pj::to_string(pj::PjValue(false)), "false");
}

TEST(PJAPI, ToStringNull) {
    // Implementation should determine: "None" or "null"
    EXPECT_EQ(pj::to_string(pj::PjValue()), "None");
}

TEST(PJAPI, ToStringNumber) {
    EXPECT_EQ(pj::to_string(pj::PjValue(123)), "123");
    EXPECT_EQ(pj::to_string(pj::PjValue(3.5)), "3.5");
}