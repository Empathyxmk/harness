#include <gtest/gtest.h>
#include "xworkflows/base.h"

TEST(PublicUsing, WorkflowEnabledInvalidSettingAndImplementationConflict) {
    // Use different workflow/field names for public case
    class AltWorkflow : public xworkflows::base::Workflow {
    public:
        AltWorkflow() : Workflow({{"begin", "Begin"}, {"end", "End"}},
                                  {{"begin_to_end", {"begin"}, "end"}},
                                  "begin") {}
    };
    class AnotherAltObj : public xworkflows::base::WorkflowEnabled {
    public:
        AnotherAltObj() : WorkflowEnabled(new AltWorkflow()) {}
    };
    AnotherAltObj obj;
    // Setting to arbitrary state
    EXPECT_THROW(obj.state = xworkflows::base::State("unknown_state", "No State"), std::invalid_argument);
    // Assigning int (invalid type) to state - should throw ValueError (invalid_argument)
    EXPECT_THROW(obj.state = 98765, std::invalid_argument);
}