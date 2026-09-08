#include <gtest/gtest.h>
#include "pj.h"

TEST(PJAPIPublic, ToStringDictDiff) {
    pj::PjValue d = pj::PjValue::object({{"x", pj::PjValue(false)}, {"y", pj::PjValue(3.14)}});
    std::string s = pj::to_string(d);
    bool match = (s == "{\"x\": false, \"y\": 3.14}" || s == "{\"y\": 3.14, \"x\": false}");
    EXPECT_TRUE(match);
    pj::PjValue r = pj::from_string(s);
    EXPECT_EQ(r, d);
}

TEST(PJAPIPublic, ToStringListDiff) {
    pj::PjValue arr = pj::PjValue::array({pj::PjValue(10), pj::PjValue(99), pj::PjValue("foo")});
    std::string s = pj::to_string(arr);
    EXPECT_EQ(s, "[10, 99, \"foo\"]");
    std::string input = "{\"b\": " + s + "}";
    pj::PjValue r = pj::from_string(input);
    pj::PjValue expected = pj::PjValue::object({{"b", arr}});
    EXPECT_EQ(r, expected);
}

TEST(PJAPIPublic, ToStringStrDiff) {
    EXPECT_EQ(pj::to_string(pj::PjValue("xyz")), "\"xyz\"");
}

TEST(PJAPIPublic, ToStringBoolDiff) {
    EXPECT_EQ(pj::to_string(pj::PjValue(false)), "false");
    EXPECT_EQ(pj::to_string(pj::PjValue(true)), "true");
}

TEST(PJAPIPublic, ToStringNullDiff) {
    EXPECT_EQ(pj::to_string(pj::PjValue()), "None");
}

TEST(PJAPIPublic, ToStringNumberDiff) {
    EXPECT_EQ(pj::to_string(pj::PjValue(42)), "42");
    EXPECT_EQ(pj::to_string(pj::PjValue(2.718)), "2.718");
}