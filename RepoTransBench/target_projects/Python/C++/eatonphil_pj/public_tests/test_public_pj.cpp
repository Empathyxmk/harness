#include <gtest/gtest.h>
#include "pj.h"

TEST(StringMethodsPublic, ObjectMultipleKeys) {
    EXPECT_EQ(
        pj::from_string("{\"alpha\":42, \"beta\":\"xyz\"}"),
        pj::PjValue::object({{"alpha", pj::PjValue(42)}, {"beta", pj::PjValue("xyz")}})
    );
}

TEST(StringMethodsPublic, ObjectArrayNumbers) {
    EXPECT_EQ(
        pj::from_string("{\"nums\":[7,8,9]}"),
        pj::PjValue::object({{"nums", pj::PjValue::array({pj::PjValue(7), pj::PjValue(8), pj::PjValue(9)})}})
    );
}

TEST(StringMethodsPublic, ObjectBoolean) {
    EXPECT_EQ(
        pj::from_string("{\"success\":false}"),
        pj::PjValue::object({{"success", pj::PjValue(false)}})
    );
}

TEST(StringMethodsPublic, ObjectWithNull) {
    EXPECT_EQ(
        pj::from_string("{\"unset\":null}"),
        pj::PjValue::object({{"unset", pj::PjValue()}})
    );
}

TEST(StringMethodsPublic, ObjectWithFloat) {
    EXPECT_EQ(
        pj::from_string("{\"value\":2.718}"),
        pj::PjValue::object({{"value", pj::PjValue(2.718)}})
    );
}

TEST(StringMethodsPublic, NestedArray) {
    EXPECT_EQ(
        pj::from_string("{\"arr\":[[1,2],[],[3]]}"),
        pj::PjValue::object({
            {"arr", pj::PjValue::array({
                pj::PjValue::array({pj::PjValue(1), pj::PjValue(2)}),
                pj::PjValue::array({}),
                pj::PjValue::array({pj::PjValue(3)})
            })}
        })
    );
}

TEST(StringMethodsPublic, NestedObjectMultipleLevels) {
    EXPECT_EQ(
        pj::from_string("{\"outer\":{\"inner\":{\"leaf\":10}}}"),
        pj::PjValue::object({
            {"outer", pj::PjValue::object({
                {"inner", pj::PjValue::object({
                    {"leaf", pj::PjValue(10)}
                })}
            })}
        })
    );
}

TEST(StringMethodsPublic, ArrayOfObjects) {
    EXPECT_EQ(
        pj::from_string("{\"users\":[{\"id\":1},{\"id\":2}]}"),
        pj::PjValue::object({
            {"users", pj::PjValue::array({
                pj::PjValue::object({{"id", pj::PjValue(1)}}),
                pj::PjValue::object({{"id", pj::PjValue(2)}})
            })}
        })
    );
}

TEST(StringMethodsPublic, BasicStringWithWhitespace) {
    EXPECT_EQ(
        pj::from_string("{   \"k\"    :   \"v\"   }"),
        pj::PjValue::object({{"k", pj::PjValue("v")}})
    );
}

TEST(StringMethodsPublic, ZeroInt) {
    EXPECT_EQ(
        pj::from_string("{\"z\":0}"),
        pj::PjValue::object({{"z", pj::PjValue(0)}})
    );
}