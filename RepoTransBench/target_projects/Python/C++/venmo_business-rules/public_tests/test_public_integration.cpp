#include <gtest/gtest.h>
#include "business_rules/engine.h"
#include "business_rules/variables.h"
#include "business_rules/actions.h"
#include "business_rules/fields.h"

class PublicVariables : public BaseVariables {
public:
    std::string bar() { return "bar"; }
    int twenty() { return 20; }
    bool false_bool() { return false; }
};

class PublicActions : public BaseActions {
public:
    void another_action(int bar) {}
    void different_action(const std::string& baz) {}
    void more_select_action(const std::string& qux) {}
};

TEST(PublicIntegrationTests, true_boolean_variable_public) {
    Condition condition{ "false_bool", "is_false", "" };
    PublicVariables vars;
    EXPECT_TRUE(check_condition(condition, vars));
}

// Port the rest of the public integration tests in this style.