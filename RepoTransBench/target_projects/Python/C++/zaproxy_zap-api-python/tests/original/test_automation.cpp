#include <gtest/gtest.h>
#include "AutomationModule.h"
#include "DummyZAP.h"
#include <map>

class AutomationTest : public ::testing::Test {
protected:
    DummyZAP dummyZap;
    Automation* automation;
    void SetUp() override {
        automation = new Automation(&dummyZap);
    }
    void TearDown() override {
        delete automation;
    }
};

TEST_F(AutomationTest, PlanProgress) {
    auto v = automation->plan_progress("myplan");
    ASSERT_EQ(v["value"], "dummy");
}

TEST_F(AutomationTest, RunPlan) {
    ASSERT_EQ(automation->run_plan("/tmp/file.yaml"), "dummy");
}

TEST_F(AutomationTest, EndDelayJob) {
    ASSERT_EQ(automation->end_delay_job(), "dummy");
}