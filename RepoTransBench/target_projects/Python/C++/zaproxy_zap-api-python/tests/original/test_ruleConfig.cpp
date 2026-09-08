#include <gtest/gtest.h>
#include "RuleConfigModule.h"
#include "DummyZAP.h"

class RuleConfigTest : public ::testing::Test {
protected:
    DummyZAP dummyZap;
    RuleConfig* ruleconfig;
    void SetUp() override {
        ruleconfig = new RuleConfig(&dummyZap);
    }
    void TearDown() override {
        delete ruleconfig;
    }
};

TEST_F(RuleConfigTest, RuleConfigValue) {
    ASSERT_EQ(ruleconfig->rule_config_value("key1"), "dummy");
}
TEST_F(RuleConfigTest, AllRuleConfigs) {
    ASSERT_EQ(ruleconfig->all_rule_configs(), "dummy");
}
TEST_F(RuleConfigTest, ResetRuleConfigValue) {
    ASSERT_EQ(ruleconfig->reset_rule_config_value("key2"), "dummy");
}
TEST_F(RuleConfigTest, ResetAllRuleConfigValues) {
    ASSERT_EQ(ruleconfig->reset_all_rule_config_values(), "dummy");
}
TEST_F(RuleConfigTest, SetRuleConfigValueWithoutValue) {
    ASSERT_EQ(ruleconfig->set_rule_config_value("key3"), "dummy");
}
TEST_F(RuleConfigTest, SetRuleConfigValueWithValue) {
    ASSERT_EQ(ruleconfig->set_rule_config_value("key4", "somevalue"), "dummy");
}