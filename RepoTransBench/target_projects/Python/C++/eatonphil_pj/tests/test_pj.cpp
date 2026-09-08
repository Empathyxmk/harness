#include <gtest/gtest.h>
#include "pj.h"

TEST(StringMethods, EmptyObject) {
    EXPECT_EQ(pj::from_string("{}"), pj::PjValue::object({}));
}

TEST(StringMethods, BasicObject) {
    EXPECT_EQ(pj::from_string("{\"foo\":\"bar\"}"),
              pj::PjValue::object({{"foo", pj::PjValue("bar")}}));
}

TEST(StringMethods, BasicNumber) {
    EXPECT_EQ(pj::from_string("{\"foo\":1}"),
              pj::PjValue::object({{"foo", pj::PjValue(1)}}));
}

TEST(StringMethods, EmptyArray) {
    EXPECT_EQ(pj::from_string("{\"foo\":[]}"),
              pj::PjValue::object({{"foo", pj::PjValue::array({})}}));
}

TEST(StringMethods, BasicArray) {
    EXPECT_EQ(pj::from_string("{\"foo\":[1,2,\"three\"]}"),
              pj::PjValue::object({{"foo", pj::PjValue::array({pj::PjValue(1), pj::PjValue(2), pj::PjValue("three")})}}));
}

TEST(StringMethods, NestedObject) {
    EXPECT_EQ(pj::from_string("{\"foo\":{\"bar\":2}}"),
              pj::PjValue::object({{"foo", pj::PjValue::object({{"bar", pj::PjValue(2)}})}}));
}

TEST(StringMethods, TrueValue) {
    EXPECT_EQ(pj::from_string("{\"foo\":true}"),
              pj::PjValue::object({{"foo", pj::PjValue(true)}}));
}

TEST(StringMethods, FalseValue) {
    EXPECT_EQ(pj::from_string("{\"foo\":false}"),
              pj::PjValue::object({{"foo", pj::PjValue(false)}}));
}

TEST(StringMethods, NullValue) {
    EXPECT_EQ(pj::from_string("{\"foo\":null}"),
              pj::PjValue::object({{"foo", pj::PjValue()}})); // PjValue() = null
}

TEST(StringMethods, BasicWhitespace) {
    EXPECT_EQ(pj::from_string("{ \"foo\" : [1, 2, \"three\"] }"),
              pj::PjValue::object({{"foo", pj::PjValue::array({pj::PjValue(1), pj::PjValue(2), pj::PjValue("three")})}}));
}

// Add main for standalone run if needed
/*
int main(int argc, char** argv) {
    ::testing::InitGoogleTest(&argc, argv);
    return RUN_ALL_TESTS();
}
*/