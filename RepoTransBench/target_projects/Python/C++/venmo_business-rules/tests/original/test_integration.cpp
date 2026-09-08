#include <gtest/gtest.h>
#include <string>
#include <map>
#include <vector>
#include "business_rules/engine.h"
#include "business_rules/variables.h"
#include "business_rules/actions.h"
#include "business_rules/fields.h"
#include "business_rules/utils.h"

class SomeVariables : public BaseVariables {
public:
    std::string foo() const { return "foo"; }
    int ten() const { return 10; }
    bool true_bool() const { return true; }
};

class SomeActions : public BaseActions {
public:
    void some_action(int foo) {}
    void some_other_action(const std::string& bar) {}
    void some_select_action(const std::string& baz) {}
};

TEST(IntegrationTests, test_true_boolean_variable) {
    Condition condition{ "true_bool", "is_true", "" };
    SomeVariables vars;
    EXPECT_TRUE(check_condition(condition, vars));
}

TEST(IntegrationTests, test_false_boolean_variable) {
    Condition condition{ "true_bool", "is_false", "" };
    SomeVariables vars;
    EXPECT_FALSE(check_condition(condition, vars));
}

TEST(IntegrationTests, test_check_true_condition_happy_path) {
    Condition condition{ "foo", "contains", "o" };
    SomeVariables vars;
    EXPECT_TRUE(check_condition(condition, vars));
}

TEST(IntegrationTests, test_check_false_condition_happy_path) {
    Condition condition{ "foo", "contains", "m" };
    SomeVariables vars;
    EXPECT_FALSE(check_condition(condition, vars));
}

// Continue porting every other Python unittest as a TEST() here, using appropriate C++ stubs & types