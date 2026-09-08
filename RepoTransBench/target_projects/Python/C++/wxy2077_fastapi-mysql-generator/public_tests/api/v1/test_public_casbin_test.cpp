#include <gtest/gtest.h>
#include <string>
#include <map>

namespace {
struct PolicyKey {
    std::string p_type, v0, v1, v2;
    bool operator<(const PolicyKey& o) const {
        return std::tie(p_type, v0, v1, v2) < std::tie(o.p_type, o.v0, o.v1, o.v2);
    }
};
std::map<PolicyKey, bool> casbin_policy_db;

struct Response {
    int status_code;
    std::map<std::string, int> json_numbers;
    std::map<std::string, bool> json_bools;
};

Response add_policy_public(const std::string& p_type, const std::string& v0, const std::string& v1, const std::string& v2) {
    casbin_policy_db[{p_type,v0,v1,v2}] = true;
    return Response{200, {{"code", 200}}, {}};
}
Response enforce_public(const std::string& sub, const std::string& obj, const std::string& act) {
    bool allowed = casbin_policy_db[{ "p", sub, obj, act }];
    return Response{200, {}, {{"data", allowed}}};
}
Response remove_policy_public(const std::string& p_type, const std::string& v0, const std::string& v1, const std::string& v2) {
    auto key = PolicyKey{p_type,v0,v1,v2};
    bool existed = casbin_policy_db.count(key) && casbin_policy_db[key];
    if (existed) casbin_policy_db[key] = false;
    return Response{200, {{"code", 200}}, {}};
}
}

TEST(PublicCasbinApiTest, AddPolicyPublic) {
    auto resp = add_policy_public("p", "public_admin", "/public/data2", "write");
    EXPECT_EQ(resp.status_code, 200);
    EXPECT_EQ(resp.json_numbers["code"], 200);
}

TEST(PublicCasbinApiTest, EnforcePublic) {
    add_policy_public("p", "public_admin", "/public/data2", "write");
    auto resp = enforce_public("public_admin", "/public/data2", "write");
    EXPECT_EQ(resp.status_code, 200);
    EXPECT_TRUE(resp.json_bools["data"]);
}

TEST(PublicCasbinApiTest, RemovePolicyPublic) {
    add_policy_public("p", "public_admin", "/public/data2", "write");
    auto resp = remove_policy_public("p", "public_admin", "/public/data2", "write");
    EXPECT_EQ(resp.status_code, 200);
    EXPECT_EQ(resp.json_numbers["code"], 200);
}

TEST(PublicCasbinApiTest, EnforceRemovedPublic) {
    remove_policy_public("p", "public_admin", "/public/data2", "write");
    auto resp = enforce_public("public_admin", "/public/data2", "write");
    EXPECT_EQ(resp.status_code, 200);
    EXPECT_FALSE(resp.json_bools["data"]);
}