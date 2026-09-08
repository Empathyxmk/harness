#include <gtest/gtest.h>
#include <string>
#include <vector>
#include <stdexcept>

// Stubs for business_rules classes/functions
#include "business_rules/actions.h"
#include "business_rules/fields.h"

class SomeActions : public BaseActions {
public:
    std::string some_action(const std::string& foo) { return "blah"; }
    std::string non_action() { return "baz"; }
};

TEST(ActionsClassTests, base_has_no_actions) {
    EXPECT_EQ(BaseActions::get_all_actions().size(), 0);
}

TEST(ActionsClassTests, get_all_actions) {
    // Simulate rule_action
    std::vector<ActionMetadata> actions = SomeActions::get_all_actions();
    ASSERT_EQ(actions.size(), 1);
    EXPECT_EQ(actions[0].name, "some_action");
    EXPECT_EQ(actions[0].label, "Some Action");
    EXPECT_EQ(actions[0].params.size(), 1);
    EXPECT_EQ(actions[0].params[0].fieldType, FIELD_TEXT);
    EXPECT_EQ(actions[0].params[0].name, "foo");
    EXPECT_EQ(actions[0].params[0].label, "Foo");

    // should work on an instance of the class too
    SomeActions sa;
    EXPECT_EQ(sa.get_all_actions().size(), 1);
}

TEST(ActionsClassTests, rule_action_doesnt_allow_unknown_field_types) {
    try {
        // Try to create a rule_action with an invalid field type (should throw)
        auto bad_action = [](){ rule_action("blah", "foo"); };
        bad_action();
        FAIL() << "Expected std::invalid_argument";
    } catch(const std::invalid_argument& e) {
        std::string msg = e.what();
        EXPECT_NE(msg.find("Unknown field type blah specified for action some_action param foo"), std::string::npos);
    } catch(...) {
        FAIL() << "Expected std::invalid_argument";
    }
}

TEST(ActionsClassTests, rule_action_doesnt_allow_unknown_parameter_name) {
    try {
        // Try to create a rule_action with a non-matching parameter name
        auto bad_action = [](){ rule_action("blah", "foo"); }; // missing required param in the function signature
        bad_action();
        FAIL() << "Expected std::invalid_argument";
    } catch(const std::invalid_argument& e) {
        std::string msg = e.what();
        EXPECT_NE(msg.find("Unknown parameter name foo specified for action some_action"), std::string::npos);
    } catch(...) {
        FAIL() << "Expected std::invalid_argument";
    }
}

TEST(ActionsClassTests, rule_action_with_no_params_or_label) {
    // You should allow a rule_action to be defined without params or label
    auto some_action = rule_action("", "");
    EXPECT_TRUE(some_action.is_rule_action);
}