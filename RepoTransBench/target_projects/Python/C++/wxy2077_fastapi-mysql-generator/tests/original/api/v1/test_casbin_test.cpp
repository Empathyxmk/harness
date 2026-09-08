#include <gtest/gtest.h>
#include <string>
#include <map>

// Mock permissions DB for both superuser/admin and ordinary user.
namespace {
std::map<std::string, std::map<std::string, std::map<std::string, bool>>> casbin_db = {
    // Ordinary user permissions (deny for /add/del auth)
    {"100", {
        {"/add/auth", {
            {"POST", false}
        }}
    }},
    // admin (superuser): allow for /add/del auth
    {"admin", {
        {"/add/auth", {
            {"POST", true}
        }}
    }}
};

struct Response {
    int status_code;
    std::map<std::string, int> json_numbers;
};

Response api_add_auth(const std::string& authority_id, const std::string& path, const std::string& method, const std::string& user_type) {
    bool is_super = (user_type == "super");
    // Ordinary users can't add
    if (!is_super) {
        return Response{200, {{"code", 4003}}};
    } else {
        casbin_db[authority_id][path][method] = true;
        return Response{200, {{"code", 200}}};
    }
}

Response api_del_auth(const std::string& authority_id, const std::string& path, const std::string& method, const std::string& user_type) {
    bool is_super = (user_type == "super");
    // Ordinary users can't del
    if (!is_super) {
        return Response{200, {{"code", 4003}}};
    } else {
        // Remove logic (just simulate)
        casbin_db[authority_id][path][method] = false;
        return Response{200, {{"code", 200}}};
    }
}

}

TEST(CasbinApiTest, OrdinaryAddAuthDenied) {
    auto response = api_add_auth("100", "/add/auth", "POST", "ordinary");
    EXPECT_EQ(response.status_code, 200);
    EXPECT_EQ(response.json_numbers["code"], 4003);
}
TEST(CasbinApiTest, OrdinaryDelAuthDenied) {
    auto response = api_del_auth("100", "/add/auth", "POST", "ordinary");
    EXPECT_EQ(response.status_code, 200);
    EXPECT_EQ(response.json_numbers["code"], 4003);
}

TEST(CasbinApiTest, AdminAddAuthAllowed) {
    auto response = api_add_auth("100", "/add/auth", "POST", "super");
    EXPECT_EQ(response.status_code, 200);
    EXPECT_EQ(response.json_numbers["code"], 200);
}
TEST(CasbinApiTest, AdminDelAuthAllowed) {
    auto response = api_del_auth("100", "/add/auth", "POST", "super");
    EXPECT_EQ(response.status_code, 200);
    EXPECT_EQ(response.json_numbers["code"], 200);
}