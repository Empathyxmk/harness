#include <gtest/gtest.h>
#include <string>
#include <vector>
#include <map>
#include <set>

// Mocks/stubs for Casbin API (for demonstration)
namespace casbin {
    static std::set<std::tuple<std::string, std::string, std::string>> policies;

    class Enforcer {
    public:
        Enforcer(const std::string& model, const std::string& policy, bool autoLoad) {
            (void)model; (void)policy; (void)autoLoad;
            // Pre-load for demo logic. In a real test, load from file.
            policies.clear();
            policies.insert({"nick", "data1", "read"});
        }
        Enforcer(const std::string& model, int /*adapter*/, bool autoLoad) {
            (void)model; (void)autoLoad;
            policies.clear();
        }
        bool enforce(const std::string& sub, const std::string& obj, const std::string& act) {
            return policies.count({sub, obj, act}) > 0;
        }
        bool add_policy(const std::string& sub, const std::string& obj, const std::string& act) {
            policies.insert({sub, obj, act});
            return true;
        }
        bool remove_policy(const std::string& sub, const std::string& obj, const std::string& act) {
            return policies.erase({sub, obj, act}) > 0;
        }
        void add_function(const std::string&, bool(*)(const std::string&, const std::string&)) {}
    };

    namespace util {
        bool key_match2(const std::string& k1, const std::string& k2) {
            // Simplified key_match2. Real Casbin has complex matching.
            return k1 == k2;
        }
    }

    class Adapter {
    public:
        Adapter(const std::string& db_url) { (void)db_url; }
    };
}

using namespace casbin;

TEST(DemoCasbinExamplesTest, DemoEnforcement) {
    // Mimic Python: model_path and policy_path don't matter (file IO omitted for demo)
    Enforcer e("model.conf", "policy.csv", true);
    // Should permit nick to read data1
    EXPECT_TRUE(e.enforce("nick", "data1", "read"));
    // Should deny nick to write data1
    EXPECT_FALSE(e.enforce("nick", "data1", "write"));
    // Add a new policy and test
    EXPECT_TRUE(e.add_policy("alice", "data2", "read"));
    EXPECT_TRUE(e.enforce("alice", "data2", "read"));
    // Remove and test
    EXPECT_TRUE(e.remove_policy("alice", "data2", "read"));
    EXPECT_FALSE(e.enforce("alice", "data2", "read"));
}

TEST(DemoCasbinExamplesTest, OrmAdapter) {
    // Simulate db_url and adapter
    std::string db_url = "sqlite:///file.db";
    casbin::Adapter adapter(db_url);
    Enforcer e("model.conf", 0, true);
    EXPECT_TRUE(e.add_policy("bob", "resource1", "read"));
    EXPECT_TRUE(e.enforce("bob", "resource1", "read"));
    EXPECT_TRUE(e.remove_policy("bob", "resource1", "read"));
    EXPECT_FALSE(e.enforce("bob", "resource1", "read"));
}

bool ParamsMatch(const std::string& full_name_k1, const std::string& key2) {
    std::string key1 = full_name_k1.substr(0, full_name_k1.find('?'));
    return casbin::util::key_match2(key1, key2);
}

TEST(DemoCasbinExamplesTest, CustomOrmParamMatch) {
    casbin::Adapter adapter("sqlite:///memory.db");
    Enforcer e("custom_model.conf", 0, true);

    // Add custom ParamsMatch function
    e.add_function("ParamsMatch", ParamsMatch);

    // Add policy for GET on /api/user
    EXPECT_TRUE(e.add_policy("999", "/api/user", "GET"));
    // Permit GET on /api/user?aaa=1
    EXPECT_TRUE(e.enforce("999", "/api/user?aaa=1", "GET"));
    // Deny GET on /api/admin?aaa=1
    EXPECT_FALSE(e.enforce("999", "/api/admin?aaa=1", "GET"));
    // Remove
    EXPECT_TRUE(e.remove_policy("999", "/api/user", "GET"));
    EXPECT_FALSE(e.enforce("999", "/api/user?aaa=1", "GET"));
}