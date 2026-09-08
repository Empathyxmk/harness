#include <gtest/gtest.h>
#include <string>
#include <unordered_map>
#include <map>

// Simulate stripping out a variable with public prefix
TEST(TestPublicVariables, PublicBasicVarStrip) {
    std::map<std::string, int> d{ {"public_private", 123}, {"should_keep", 456} };
    std::map<std::string, int> result;
    for (const auto& kv : d) {
        if (kv.first.rfind("public_", 0) != 0) // not starting with "public_"
            result.insert(kv);
    }
    EXPECT_TRUE(result.count("should_keep") == 1);
    EXPECT_TRUE(result.count("public_private") == 0);
}

TEST(TestPublicVariables, PublicGroupVarPrecedence) {
    std::map<std::string, std::string> group_vars = { {"pubkey", "groupval"}, {"shared", "gshared"} };
    std::map<std::string, std::string> host_vars = { {"pubkey", "hostval"}, {"override", "hval"}, {"shared", "hshared"} };
    std::map<std::string, std::string> merged_vars = group_vars;
    merged_vars.insert(host_vars.begin(), host_vars.end());
    EXPECT_EQ(merged_vars["pubkey"], "hostval");
    EXPECT_EQ(merged_vars["shared"], "hshared");
    EXPECT_EQ(merged_vars["override"], "hval");
    EXPECT_TRUE(
        std::find_if(merged_vars.begin(), merged_vars.end(), [](const auto& p) { return p.second == "groupval"; }) == merged_vars.end()
    );
}

TEST(TestPublicVariables, PublicNestedVars) {
    std::map<std::string, std::map<std::string, int>> outer{ {"outer", {{"public_hidden", 2}, {"visible", 42}}} };
    outer["plain"] = {};
    // Remove keys starting with "public_" in nested dicts
    for (auto& [k, vdict] : outer) {
        for (auto it = vdict.begin(); it != vdict.end();) {
            if (it->first.rfind("public_", 0) == 0)
                it = vdict.erase(it);
            else
                ++it;
        }
    }
    // Reconstruct result
    EXPECT_TRUE(outer.count("plain"));
    EXPECT_TRUE(outer.count("outer"));
    EXPECT_TRUE(outer["outer"].count("public_hidden") == 0);
    EXPECT_TRUE(outer["outer"].count("visible") == 1);
}