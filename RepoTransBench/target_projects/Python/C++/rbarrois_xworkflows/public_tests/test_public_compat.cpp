#include <gtest/gtest.h>
#include "xworkflows/base.h"

TEST(PublicCompat, StringTypeIsStdString) {
    EXPECT_TRUE(typeid(xworkflows::base::Workflow::static_type_name()).hash_code() == typeid(std::string).hash_code());
}

// Base Workflow has states mapped/subscripted
TEST(PublicCompat, BaseWorkflowHasStates) {
    xworkflows::base::Workflow AltCompWorkflow{
        {{"alpha", "Alpha"}, {"beta", "Beta"}},
        {{"ab", {"alpha"}, "beta"}},
        "alpha"
    };
    auto& workflow = AltCompWorkflow;
    EXPECT_TRUE(workflow.states.find("alpha") != workflow.states.end());
    EXPECT_EQ(workflow.states.at("beta").title, "Beta");
}