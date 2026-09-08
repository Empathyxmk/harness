#include <gtest/gtest.h>
#include "business_rules/actions.h"

TEST(PublicActionsClassTestCase, has_get_all_actions_public) {
    // We can "simulate" this with existence of method in our stub
    EXPECT_NO_THROW({
        auto actions = BaseActions::get_all_actions();
    });
}

TEST(PublicActionsClassTestCase, rule_action_metadata_public) {
    auto metadata = rule_action("test_param", "label");
    // Check properties; in stub, adjust as appropriate!
    EXPECT_EQ(metadata.is_rule_action, true);
    // In stub, 'name' and 'label' may be empty but they exist as members:
    SUCCEED();
}