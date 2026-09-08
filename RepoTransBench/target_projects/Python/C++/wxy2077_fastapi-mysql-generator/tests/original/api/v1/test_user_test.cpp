#include <gtest/gtest.h>
#include <string>
#include <map>
// Mock user registry and API

namespace {
struct User {
    std::string username;
    std::string password;
    std::string nickname;
};
std::map<std::string, User> user_db = {
    {"test@test.com", {"test@test.com", "test", "Testy"}},
    {"admin@admin.com", {"admin@admin.com", "admin", "Admin"}}
};

std::string create_token_for_user(const std::string& username) {
    return "token_" + username;
}

bool token_valid(const std::string& token) {
    return token.find("token_") == 0;
}

struct Response {
    int status_code;
    std::map<std::string, int> json_numbers;
    std::map<std::string, std::string> json_strings;
};

Response post_login(const std::string& username, const std::string& password) {
    auto it = user_db.find(username);
    if (it != user_db.end() && it->second.password == password) {
        return Response{200, {{"code", 200}}, {{"token", create_token_for_user(username)}}, };
    } else if (it != user_db.end()) {
        return Response{200, {{"code", 4003}}, {}};
    }
    return Response{200, {{"code", 4003}}, {}};
}

Response get_user_info(const std::string& token) {
    // Token: token_...
    for (const auto& kv : user_db) {
        if (token == create_token_for_user(kv.first)) {
            return Response{200, {{"code", 200}}, {{"nickname", kv.second.nickname}}};
        }
    }
    return Response{200, {{"code", 4003}}, {}};
}

}

TEST(UserApiTest, Login) {
    auto response = post_login("test@test.com", "test");
    EXPECT_EQ(response.status_code, 200);
    EXPECT_EQ(response.json_numbers["code"], 200);
    EXPECT_TRUE(response.json_strings["token"].find("token_") == 0);
}

TEST(UserApiTest, ErrorLogin) {
    auto response = post_login("test1@test.com", "t");
    EXPECT_EQ(response.status_code, 200);
    EXPECT_EQ(response.json_numbers["code"], 4003);
}

TEST(UserApiTest, GetUser) {
    auto resp = post_login("test@test.com", "test");
    ASSERT_EQ(resp.status_code, 200);
    std::string token = resp.json_strings["token"];
    auto response = get_user_info(token);
    EXPECT_EQ(response.status_code, 200);
    EXPECT_EQ(response.json_numbers["code"], 200);
    EXPECT_FALSE(response.json_strings["nickname"].empty());
}