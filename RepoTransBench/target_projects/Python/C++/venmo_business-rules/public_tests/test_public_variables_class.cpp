#include <gtest/gtest.h>
#include "business_rules/variables.h"
#include "business_rules/operators.h"

class PublicSomeVariables : public BaseVariables {
public:
    std::string another_rule() { return "different"; }
    std::string non_rule_func() { return "should not be a variable"; }
};

TEST(PublicVariablesClassTests, base_has_no_variables_public) {
    EXPECT_EQ(BaseVariables::get_all_variables().size(), 0);
}

TEST(PublicVariablesClassTests, get_all_variables_public) {
    std::vector<VariableMetadata> vars = PublicSomeVariables::get_all_variables();
    ASSERT_EQ(vars.size(), 1);
    EXPECT_EQ(vars[0].name, "another_rule");
    EXPECT_EQ(vars[0].label, "Public Rule Label");
    EXPECT_EQ(vars[0].field_type, "string");
    EXPECT_TRUE(vars[0].options.empty());

    PublicSomeVariables instance;
    EXPECT_EQ(instance.get_all_variables().size(), 1);
}