#include <gtest/gtest.h>
#include "gitignore_parser.h"

using namespace gitignore;

TEST(TestAdvancedRuleParsing, SomeErrorBranches) {
    // In Python: rule = rule_from_pattern('/////')
    // The code returns an IgnoreRule for '/////'.
    auto rule = rule_from_pattern("/////");
    ASSERT_TRUE(rule != nullptr);
    EXPECT_EQ(rule->pattern, "/////");
}