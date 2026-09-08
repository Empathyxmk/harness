#include <gtest/gtest.h>
#include <string>
#include <vector>
#include "business_rules/variables.h"
#include "business_rules/operators.h"

class SomeVariables : public BaseVariables {
public:
    std::string this_is_rule_1() { return "blah"; }
    std::string non_rule() { return "baz"; }
};

TEST(VariablesClassTests, base_has_no_variables) {
    EXPECT_EQ(BaseVariables::get_all_variables().size(), 0);
}

TEST(VariablesClassTests, get_all_variables) {
    std::vector<VariableMetadata> vars = SomeVariables::get_all_variables();
    ASSERT_EQ(vars.size(), 1);
    EXPECT_EQ(vars[0].name, "this_is_rule_1");
    EXPECT_EQ(vars[0].label, "This Is Rule 1");
    EXPECT_EQ(vars[0].field_type, "string");
    EXPECT_TRUE(vars[0].options.empty());

    SomeVariables instance;
    EXPECT_EQ(instance.get_all_variables().size(), 1);
}