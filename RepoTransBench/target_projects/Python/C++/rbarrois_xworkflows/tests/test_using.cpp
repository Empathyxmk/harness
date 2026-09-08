#include <gtest/gtest.h>
#include <string>
#include <vector>
#include "xworkflows/base.h"

using namespace xworkflows;

class WorkflowDeclarationTest : public ::testing::Test {
protected:
    void AssertExpected(const base::Workflow& workflow, const std::string& initial_state = "foo") {
        EXPECT_EQ(workflow.states.size(), 3);
        EXPECT_EQ(workflow.transitions.size(), 3);
        EXPECT_EQ(workflow.states.at(initial_state), workflow.initial_state);
        EXPECT_EQ(workflow.transitions.at("foobar").source[0], workflow.states.at("foo"));
        EXPECT_EQ(workflow.transitions.at("foobar").target, workflow.states.at("bar"));

        for (const auto& entry : workflow.states) {
            std::string exp_title = entry.second.name;
            exp_title[0] = toupper(exp_title[0]);
            EXPECT_EQ(entry.second.title, exp_title);
            EXPECT_TRUE(entry.second.name == "foo" || entry.second.name == "bar" || entry.second.name == "baz");
        }
    }
};

TEST_F(WorkflowDeclarationTest, SimpleDefinition) {
    base::Workflow MyWorkflow{
        {{"foo", "Foo"}, {"bar", "Bar"}, {"baz", "Baz"}},
        {{"foobar", {"foo"}, "bar"},
         {"gobaz", {"foo", "bar"}, "baz"},
         {"bazbar", {"baz"}, "bar"}},
        "foo"
    };
    AssertExpected(MyWorkflow);
}

TEST_F(WorkflowDeclarationTest, Subclassing) {
    base::Workflow MyWorkflow{
        {{"foo", "Foo"}, {"bar", "Bar"}, {"baz", "Baz"}},
        {{"foobar", {"foo"}, "bar"},
         {"gobaz", {"foo", "bar"}, "baz"},
         {"bazbar", {"baz"}, "bar"}},
        "foo"
    };
    AssertExpected(MyWorkflow);

    auto MySubWorkflow(MyWorkflow);
    MySubWorkflow.initial_state = MySubWorkflow.states.at("bar");
    AssertExpected(MySubWorkflow, "bar");
}

TEST_F(WorkflowDeclarationTest, SubclassingAlt) {
    base::Workflow MyWorkflow{
        {{"foo", "Foo"}, {"bar", "Bar"}, {"baz", "Baz"}},
        {{"foobar", {"foo"}, "bar"},
         {"gobaz", {"foo", "bar"}, "baz"},
         {"bazbar", {"baz"}, "bar"}},
        "foo"
    };
    AssertExpected(MyWorkflow);

    base::Workflow MySubWorkflow{
        {{"bar", "BARBAR"}, {"blah", "Blah"}, {"foo", "Foo"}, {"baz", "Baz"}},
        {{"gobaz", {"foo", "bar", "blah"}, "baz"},
         {"blahblah", {"blah"}, "blah"},
         {"foobar", {"foo"}, "bar"},
         {"bazbar", {"baz"}, "bar"}},
        "bar"
    };

    EXPECT_EQ(MySubWorkflow.states.size(), 4U);
    std::vector<std::string> state_names;
    for (const auto& kv : MySubWorkflow.states) state_names.push_back(kv.first);
    EXPECT_EQ(state_names, std::vector<std::string>({"foo", "bar", "baz", "blah"}));
    EXPECT_EQ(MySubWorkflow.initial_state.name, "bar");
    EXPECT_EQ(MySubWorkflow.states.at("bar"), MySubWorkflow.initial_state);
    EXPECT_EQ(MySubWorkflow.states.at("bar").title, "BARBAR");
    EXPECT_EQ(MySubWorkflow.states.at("blah").title, "Blah");

    EXPECT_EQ(MySubWorkflow.transitions.size(), 4U);
    std::vector<std::string> tr_names;
    for (const auto& kv : MySubWorkflow.transitions) tr_names.push_back(kv.first);
    EXPECT_EQ(tr_names, std::vector<std::string>({"foobar", "gobaz", "bazbar", "blahblah"}));
    EXPECT_EQ(MySubWorkflow.transitions.at("gobaz").source.size(), 3U);
}

TEST_F(WorkflowDeclarationTest, InvalidDefinitions) {
    // Various invalid workflow setups
    EXPECT_THROW(base::Workflow(
        {{"12", "12"}, {"13", "13"}, {"14", "14"}},
        {},
        "12"
    ), std::invalid_argument);

    // Wrong state entry type
    EXPECT_THROW(base::Workflow(
        {{"1", "2"}},
        {},
        "12"
    ), std::invalid_argument);

    // Transition references a non-existent state
    EXPECT_THROW(base::Workflow(
        {{"foo", "Foo"}, {"bar", "Bar"}, {"baz", "Baz"}},
        {{"foobar", {"bbb"}, "bar"}},
        "foo"
    ), std::out_of_range);

    // Transition tuple is wrong
    EXPECT_THROW(base::Workflow(
        {{"foo", "Foo"}, {"bar", "Bar"}, {"baz", "Baz"}},
        {{"foobar", {"bbb"}, ""}},
        "foo"
    ), std::invalid_argument);
}