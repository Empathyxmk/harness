#include <gtest/gtest.h>
#include <string>
#include <vector>
#include "xworkflows/base.h"
#include "xworkflows/compat.h"

using namespace xworkflows;

TEST(StateTestCase, Definition) {
    EXPECT_THROW(base::State("a--b", "A--B"), std::invalid_argument);
}

TEST(StateTestCase, Equality) {
    base::State s1("foo", "Foo");
    base::State s2("foo", "Foo");
    EXPECT_FALSE(s1 == s2); // Different object instances
}

TEST(StateTestCase, Repr) {
    base::State a("foo", "Foo");
    std::string rep = a.repr();
    EXPECT_TRUE(rep.find("foo") != std::string::npos);
    EXPECT_TRUE(rep.find("Foo") == std::string::npos);
}

// ------ StateList --------

class StateListFixture : public ::testing::Test {
protected:
    base::State foo, bar, bar2;
    base::StateList sl;
    StateListFixture() :
        foo("foo", "Foo"), bar("bar", "Bar"), bar2("bar", "Bar"),
        sl({foo, bar}) {}
};

TEST_F(StateListFixture, Access) {
    EXPECT_EQ(sl.foo(), foo);
    EXPECT_EQ(sl["foo"], foo);
    EXPECT_FALSE(sl.has("baz"));
}

TEST_F(StateListFixture, Contains) {
    EXPECT_TRUE(sl.contains(foo));
    EXPECT_TRUE(sl.contains(bar));
    EXPECT_TRUE(sl.contains("foo"));
    EXPECT_FALSE(sl.contains(bar2));
    EXPECT_FALSE(sl.contains("bar2"));
}

TEST_F(StateListFixture, ListMethods) {
    EXPECT_TRUE(sl.size() > 0);
    EXPECT_FALSE(base::StateList({}).size() > 0);
    EXPECT_EQ(sl.size(), 2);
}

// ------ TransitionList --------

class TransitionListFixture : public ::testing::Test {
protected:
    base::State foo, bar, baz, baz2;
    base::Transition foobar, foobar2, gobaz;
    base::TransitionList tl;
    TransitionListFixture()
        : foo("foo", "Foo"), bar("bar", "Bar"), baz("baz", "Baz"), baz2("baz", "Baz"),
          foobar("foobar", foo, bar), foobar2("foobar", foo, bar),
          gobaz("gobaz", std::vector<base::State>{foo, bar}, baz),
          tl({foobar, gobaz}) {}
};

TEST_F(TransitionListFixture, Access) {
    EXPECT_EQ(tl.foobar(), foobar);
    EXPECT_EQ(tl["foobar"], foobar);
    EXPECT_FALSE(tl.has("foobaz"));
}

TEST_F(TransitionListFixture, Contains) {
    EXPECT_TRUE(tl.contains(foobar));
    EXPECT_TRUE(tl.contains(gobaz));
    EXPECT_FALSE(tl.contains(foobar2));
}

TEST_F(TransitionListFixture, ListMethods) {
    EXPECT_TRUE(tl.size() > 0);
    EXPECT_FALSE(base::TransitionList({}).size() > 0);
    EXPECT_EQ(tl.size(), 2);
}

TEST_F(TransitionListFixture, Available) {
    auto avail_foo = tl.available_from(foo);
    ASSERT_EQ(avail_foo.size(), 2);
    EXPECT_EQ(avail_foo[0], foobar);
    EXPECT_EQ(avail_foo[1], gobaz);

    auto avail_bar = tl.available_from(bar);
    ASSERT_EQ(avail_bar.size(), 1);
    EXPECT_EQ(avail_bar[0], gobaz);

    auto avail_baz = tl.available_from(baz);
    EXPECT_TRUE(avail_baz.empty());
}


// -------- StateWrapper --------

class StateWrapperFixture : public ::testing::Test {
protected:
    struct MyWorkflow : base::Workflow {
        MyWorkflow() : Workflow{
            {{"foo", "Foo"}, {"bar", "Bar"}, {"baz", "Baz"}},
            {{"foobar", {"foo"}, "bar"},
             {"gobaz", {"foo", "bar"}, "baz"},
             {"bazbar", {"baz"}, "bar"}},
            "foo"}{}
    };
    base::State foo, bar;
    base::Workflow *wf;
    base::StateWrapper sf, sf2;

    StateWrapperFixture() : foo("foo", "Foo"), bar("bar", "Bar"),
        wf(new MyWorkflow()), sf(foo, *wf), sf2(foo, *wf) {}
    ~StateWrapperFixture() { delete wf; }
};

TEST_F(StateWrapperFixture, Comparison) {
    EXPECT_EQ(sf, sf2);
    EXPECT_EQ(sf, foo);
    EXPECT_EQ(foo, sf);
    EXPECT_NE(sf, bar);
    EXPECT_NE(sf, 0);
    EXPECT_NE(bar, sf);
    EXPECT_EQ(sf, std::string("foo"));
    EXPECT_EQ(std::string("foo"), sf);
}

TEST_F(StateWrapperFixture, Attributes) {
    EXPECT_TRUE(sf.is_foo());
    EXPECT_FALSE(sf.is_bar());
    EXPECT_FALSE(sf.has("foo"));
    EXPECT_EQ(foo.name, sf.name);
    EXPECT_EQ(foo.title, sf.title);

    struct BadSubclass : base::StateWrapper {
        BadSubclass() : base::StateWrapper(base::State("foo", "Foo"), *(new base::Workflow())) {
            // access state before it's set - simulate error
            auto x = this->state;
        }
    };
    EXPECT_THROW(BadSubclass(), std::exception);
}

TEST_F(StateWrapperFixture, Representation) {
    EXPECT_EQ(sf.str(), foo.str());
    EXPECT_TRUE(sf.repr().find(foo.repr()) != std::string::npos);
    EXPECT_EQ(sf.name, compat::u(sf));
    EXPECT_EQ(std::hash<std::string>{}(foo.name), std::hash<std::string>{}(sf.name));
}

// --------- WorkflowEnabled --------

class WorkflowEnabledTestCase : public ::testing::Test {
protected:
    struct MyWorkflow;
    struct MyWorkflowEnabled;
    base::State foo, bar;
    base::Workflow* wf;
    MyWorkflowEnabled* wfe;

    WorkflowEnabledTestCase();
    ~WorkflowEnabledTestCase();
};

struct WorkflowEnabledTestCase::MyWorkflow : base::Workflow {
    MyWorkflow() : Workflow{
        {{"foo", "Foo"}, {"bar", "Bar"}, {"baz", "Baz"}},
        {{"foobar", {"foo"}, "bar"},
         {"gobaz", {"foo", "bar"}, "baz"},
         {"bazbar", {"baz"}, "bar"}},
        "foo"}{}
};

struct WorkflowEnabledTestCase::MyWorkflowEnabled : base::WorkflowEnabled {
    MyWorkflowEnabled() : base::WorkflowEnabled(new MyWorkflow()) {}
};

WorkflowEnabledTestCase::WorkflowEnabledTestCase()
    : foo("foo", "Foo"), bar("bar", "Bar"), wf(new MyWorkflow()),
      wfe(new MyWorkflowEnabled()) {}

WorkflowEnabledTestCase::~WorkflowEnabledTestCase() {
    delete wf;
    delete wfe;
}

TEST_F(WorkflowEnabledTestCase, AccessState) {
    auto obj = wfe;
    EXPECT_EQ(obj->state, foo);
    EXPECT_TRUE(obj->state.is_foo());
    EXPECT_FALSE(obj->state.is_bar());

    obj->state = bar;

    EXPECT_EQ(obj->state, bar);
    EXPECT_TRUE(obj->state.is_bar());
    EXPECT_FALSE(obj->state.is_foo());
}

TEST_F(WorkflowEnabledTestCase, CompareStateText) {
    auto obj = wfe;
    obj->state = "bar";
    EXPECT_EQ(obj->state, bar);
    EXPECT_TRUE(obj->state.is_bar());
    EXPECT_FALSE(obj->state.is_foo());
}

// The rest of the implementation for hooks, ImplementationProperty, etc., would follow similarly.