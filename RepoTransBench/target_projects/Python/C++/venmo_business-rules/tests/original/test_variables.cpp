#include <gtest/gtest.h>
#include "business_rules/utils.h"
#include "business_rules/variables.h"
#include "business_rules/operators.h"
#include <string>

TEST(RuleVariableTests, pretty_label) {
    EXPECT_EQ(fn_name_to_pretty_label("some_name_Of_a_thing"), "Some Name Of A Thing");
    EXPECT_EQ(fn_name_to_pretty_label("hi"), "Hi");
}

TEST(RuleVariableTests, rule_variable_requires_instance_of_base_type) {
    try {
        auto badFunc = [](){ rule_variable("a_string"); };
        badFunc();
        FAIL() << "Expected std::invalid_argument";
    } catch(const std::invalid_argument& e) {
        std::string msg = e.what();
        EXPECT_NE(msg.find("a_string is not instance of BaseType in rule_variable field_type"), std::string::npos);
    }
}

TEST(RuleVariableTests, rule_variable_decorator_internals) {
    auto some_test_function = [](void*){};
    auto wrapper = rule_variable(StringType, "Foo Name", {"op1", "op2"});
    auto func = wrapper(some_test_function);
    EXPECT_TRUE(func.is_rule_variable);
    EXPECT_EQ(func.label, "Foo Name");
    EXPECT_EQ(func.field_type, StringType);
    // etc.
}

// Continue porting every test function.