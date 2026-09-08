#include <gtest/gtest.h>
#include <gmock/gmock.h>
#include <string>
#include "business_rules/engine.h"
#include "business_rules/variables.h"
#include "business_rules/operators.h"
#include "business_rules/actions.h"

using namespace testing;

class EngineTests : public ::testing::Test {};

TEST_F(EngineTests, run_all_some_rule_triggered) {
    Rule rule1{ "condition1", "action name 1" };
    Rule rule2{ "condition2", "action name 2" };
    BaseVariables variables;
    BaseActions actions;

    // Mock run to only return true if action name equals "action name 1"
    ON_CALL(engine, run(_, _, _)).WillByDefault([](const Rule& rule, auto, auto){ return rule.actions == "action name 1"; });
    // Not a real syntax: actual code needs to use gmock/EXPECT_CALL properly

    bool result = engine.run_all({rule1, rule2}, variables, actions, false);
    EXPECT_TRUE(result);
    // ... More assertion stubs

    // switch order & test again, etc
}

// (The rest of the tests, following the same pattern, adapted to C++ with GoogleTest and GMock)
//
// Stub out or define mocks for engine functions where patching is needed as in Python tests.
//
// Because these tests use patching and MagicMock heavily in Python, you must define appropriate mocks for the
// engine functions, and simulate call_count and argument checks.