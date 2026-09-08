#include <gtest/gtest.h>
#include "xworkflows/base.h"

TEST(PublicBase, WorkflowStatesAndTransitions) {
    xworkflows::base::Workflow AltWorkflow{
        {{"start", "Start"}, {"mid", "Middle"}, {"end", "End"}},
        {{"go_mid", {"start"}, "mid"},
         {"finish", {"mid"}, "end"},
         {"reset", {"end"}, "start"}},
        "start"
    };
    auto& wf = AltWorkflow;
    EXPECT_EQ(wf.states.size(), 3U);
    EXPECT_EQ(wf.states.at("start").title, "Start");
    EXPECT_EQ(wf.transitions.at("go_mid").source.at(0).name, "start");
    EXPECT_EQ(wf.transitions.at("finish").target.name, "end");
    EXPECT_EQ(wf.initial_state, wf.states.at("start"));
}

TEST(PublicBase, WorkflowInvalidStateTransition) {
    // Creating a workflow that references a missing state in transition
    EXPECT_ANY_THROW({
        xworkflows::base::Workflow BadWorkflow(
            {{"x", "Ex"}, {"y", "Why"}},
            {{"invalid", {"x"}, "z"}},
            "x"
        );
    });
}