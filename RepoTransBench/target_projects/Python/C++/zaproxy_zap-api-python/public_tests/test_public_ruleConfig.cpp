#include <gtest/gtest.h>
#include <string>
#include <map>

// Dummy ruleConfig_module public API for test
struct SetRuleConfigResp {
    std::string status;
    std::string ruleId;
};
struct GetRuleConfigResp {
    std::string value;
    std::string key;
};

SetRuleConfigResp set_rule_config_value(const std::string& rule_id, const std::string& key, const std::string& value) {
    return {"UPDATED", rule_id};
}
GetRuleConfigResp get_rule_config_value(const std::string& rule_id, const std::string& key) {
    return { "LOW", key };
}

TEST(PublicRuleConfigTest, RuleConfigSetAndGetDiffData) {
    std::string rule_id = "12001";
    std::string key = "attackStrength";
    std::string value = "LOW";
    SetRuleConfigResp set_resp = set_rule_config_value(rule_id, key, value);
    ASSERT_EQ(set_resp.status, "UPDATED");
    ASSERT_EQ(set_resp.ruleId, rule_id);

    GetRuleConfigResp get_resp = get_rule_config_value(rule_id, key);
    ASSERT_EQ(get_resp.value, value);
    ASSERT_EQ(get_resp.key, key);
}