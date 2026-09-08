#include <gtest/gtest.h>
#include <string>
#include <unordered_map>
#include <set>

TEST(TestVariables, GpGroupVars) {
    std::unordered_map<std::string, std::string> gvars;
    gvars["gp_not_overridden"] = "gp";
    EXPECT_EQ(gvars["gp_not_overridden"], "gp");
    std::set<std::string> keys;
    for (auto& p : gvars) keys.insert(p.first);
    EXPECT_EQ(keys, std::set<std::string>({"gp_not_overridden"}));
}

TEST(TestVariables, ParentGroupVars) {
    std::unordered_map<std::string, std::string> pvars;
    pvars["parent_not_overridden"] = "parent";
    pvars["gp_overridden_in_parent"] = "gp";
    EXPECT_EQ(pvars["parent_not_overridden"], "parent");
    std::set<std::string> keys;
    for (auto& p : pvars) keys.insert(p.first);
    EXPECT_EQ(keys, std::set<std::string>({"parent_not_overridden", "gp_overridden_in_parent"}));
}

TEST(TestVariables, HostVars) {
    std::unordered_map<std::string, std::string> hvars;
    hvars["gp_overridden_in_child"] = "child";
    hvars["parent_overridden_in_child"] = "child";
    hvars["child_only"] = "child";
    EXPECT_EQ(hvars["gp_overridden_in_child"], "child");
    EXPECT_EQ(hvars["parent_overridden_in_child"], "child");
    EXPECT_EQ(hvars["child_only"], "child");
}