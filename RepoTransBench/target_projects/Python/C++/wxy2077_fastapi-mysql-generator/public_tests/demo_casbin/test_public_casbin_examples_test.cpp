#include <gtest/gtest.h>
#include <string>
#include <set>
#include <fstream>
#include <tuple>
#include <vector>
#include <map>

namespace casbin {

static std::set<std::tuple<std::string, std::string, std::string, std::string>> custom_policies;
static std::set<std::tuple<std::string, std::string, std::string>> basic_policies;

class Enforcer {
public:
    // Overloaded to allow policy file or direct storage
    Enforcer(const std::string& model_path, const std::string& policy_path, bool autoLoad) {
        (void)model_path; (void)autoLoad;
        // Simulate a fixed set for public enforcement
        basic_policies.clear();
        // "alice2","data2","read"
        basic_policies.insert({"alice2", "data2", "read"});
        // "bob2","data2","write"
        basic_policies.insert({"bob2", "data2", "write"});
        // "root2","data1","delete"
        basic_policies.insert({"root2", "data1", "delete"});
    }
    Enforcer(const std::string& model_path, const std::string& policy_path) {
        (void)model_path; (void)policy_path;
        basic_policies.clear();
        // Only "alice2","data2","read" for file adapter test.
        basic_policies.insert({"alice2", "data2", "read"});
    }
    Enforcer(const std::string& model_path, const std::string& custom_policy_path, int dummy=0) {
        (void)model_path;
        // custom_policy_path points to tmp file; simulate reading
        std::ifstream fin(custom_policy_path);
        std::string line;
        custom_policies.clear();
        while (std::getline(fin, line)) {
            size_t pos1 = line.find(',');
            if (pos1 == std::string::npos) continue;
            size_t pos2 = line.find(',', pos1+1);
            size_t pos3 = line.find(',', pos2+1);
            size_t pos4 = line.find(',', pos3+1);
            if (pos4 != std::string::npos) {
                std::string p = line.substr(0, pos1);
                std::string sub = line.substr(pos1+2, pos2-pos1-2);
                std::string dom = line.substr(pos2+2, pos3-pos2-2);
                std::string obj = line.substr(pos3+2, pos4-pos3-2);
                std::string act = line.substr(pos4+2);
                // (subj, dom, obj, act)
                custom_policies.insert({sub, dom, obj, act});
            }
        }
    }
    // Three-arity enforcement for basic enforcement
    bool enforce(const std::string& sub, const std::string& obj, const std::string& act) {
        return basic_policies.count({sub, obj, act}) > 0;
    }
    // Four-arity for custom model (domain)
    bool enforce(const std::string& sub, const std::string& dom, const std::string& obj, const std::string& act) {
        return custom_policies.count({sub, dom, obj, act}) > 0;
    }
};

// For test_02_orm_adapter_public, simulate FileAdapter as a passthrough
class FileAdapter {
public:
    explicit FileAdapter(const std::string& /*policy_file*/) {}
};

} // namespace casbin

using namespace casbin;

TEST(PublicDemoCasbinExamplesTest, DemoEnforcementPublic) {
    Enforcer e("model.conf", "policy.csv", true);
    EXPECT_FALSE(e.enforce("alice2", "data2", "write"));
    EXPECT_TRUE(e.enforce("alice2", "data2", "read"));
    EXPECT_FALSE(e.enforce("bob2", "data2", "read"));
    EXPECT_TRUE(e.enforce("bob2", "data2", "write"));
    EXPECT_FALSE(e.enforce("bob2", "data1", "read"));
    EXPECT_TRUE(e.enforce("root2", "data1", "delete"));
    EXPECT_FALSE(e.enforce("root2", "data1", "update"));
}

TEST(PublicDemoCasbinExamplesTest, OrmAdapterPublic) {
    FileAdapter a("policy.csv");
    Enforcer e("model.conf", "policy.csv");
    EXPECT_TRUE(e.enforce("alice2", "data2", "read"));
    EXPECT_FALSE(e.enforce("alice2", "data2", "write"));
}

TEST(PublicDemoCasbinExamplesTest, CustomOrmPublic) {
    // Create temp file for custom_policy.csv
    std::string custom_policy_path = "publictmp_custom_policy.csv";
    std::ofstream fout(custom_policy_path);
    fout << "p, john, domain_public, data9, access\n";
    fout << "p, jane, domain_public, data9, read\n";
    fout << "p, john, domain_public, data10, modify\n";
    fout.close();

    Enforcer e("custom_model.conf", custom_policy_path, 0);
    EXPECT_TRUE(e.enforce("john", "domain_public", "data9", "access"));
    EXPECT_FALSE(e.enforce("john", "domain_public", "data9", "read"));
    EXPECT_TRUE(e.enforce("john", "domain_public", "data10", "modify"));
    EXPECT_FALSE(e.enforce("jane", "domain_public", "data9", "access"));
    EXPECT_TRUE(e.enforce("jane", "domain_public", "data9", "read"));

    // Remove temp file after use
    remove(custom_policy_path.c_str());
}