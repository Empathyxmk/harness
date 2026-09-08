#include <gtest/gtest.h>
#include <string>
#include <map>
#include <vector>

// Mock for public user test registry, separate from private
namespace {
struct User {
    std::string username;
    std::string password;
    std::string nick_name;
};
std::map<std::string, User> public_user_db;

struct Response {
    int status_code;
    std::map<std::string, int> json_numbers;
    std::map<std::string, std::string> json_strings;
    std::vector<User> users_list;
};

Response create_user_public(const std::string& username, const std::string& password, const std::string& nick) {
    public_user_db[username] = {username, password, nick};
    return Response{200, {{"code", 200}}, {{"username", username}}, {}};
}
Response search_user_public(const std::string& username) {
    // Returns user if found in a vector
    std::vector<User> result;
    auto it = public_user_db.find(username);
    if (it != public_user_db.end()) result.push_back(it->second);
    return Response{200, {}, {}, result};
}
Response login_user_public(const std::string& username, const std::string& password) {
    auto it = public_user_db.find(username);
    if (it != public_user_db.end() && it->second.password == password) {
        return Response{200, {{"code", 200}}, {{"access_token", "token42"}}, {}};
    }
    return Response{200, {{"code", 4003}}, {}, {}};
}
Response update_password_public(const std::string& username, const std::string& oldpw, const std::string& newpw) {
    auto it = public_user_db.find(username);
    if (it != public_user_db.end() && it->second.password == oldpw) {
        it->second.password = newpw;
        return Response{200, {{"code", 200}}, {}, {}};
    }
    return Response{200, {{"code", 4003}}, {}, {}};
}
Response delete_user_public(const std::string& username) {
    auto it = public_user_db.find(username);
    if (it != public_user_db.end()) {
        public_user_db.erase(it);
        return Response{200, {{"code", 200}}, {}, {}};
    }
    return Response{200, {{"code", 4003}}, {}, {}};
}
}

TEST(PublicUserApiTest, CreateUserPublic) {
    std::string username = "publicuser42";
    std::string password = "publicpassword42";
    auto response = create_user_public(username, password, "PublicNick42");
    EXPECT_EQ(response.status_code, 200);
    EXPECT_EQ(response.json_numbers["code"], 200);
    EXPECT_EQ(response.json_strings["username"], username);
}
TEST(PublicUserApiTest, SearchUserPublic) {
    std::string username = "publicuser42";
    // Ensure user exists
    create_user_public(username, "pw", "nick");
    auto response = search_user_public(username);
    ASSERT_EQ(response.status_code, 200);
    int found = 0;
    for (const auto& user : response.users_list)
        if (user.username == username) found = 1;
    EXPECT_EQ(found, 1);
}
TEST(PublicUserApiTest, UserLoginPublic) {
    std::string username = "publicuser42";
    std::string password = "publicpassword42";
    create_user_public(username, password, "nick");
    auto response = login_user_public(username, password);
    EXPECT_EQ(response.status_code, 200);
    EXPECT_EQ(response.json_numbers["code"], 200);
    EXPECT_EQ(response.json_strings["access_token"], "token42");
}
TEST(PublicUserApiTest, UpdatePasswordPublic) {
    std::string username = "publicuser42";
    std::string oldpw = "publicpassword42";
    std::string newpw = "publicpassword_updated";
    create_user_public(username, oldpw, "nick");
    auto response = update_password_public(username, oldpw, newpw);
    EXPECT_EQ(response.status_code, 200);
    EXPECT_EQ(response.json_numbers["code"], 200);
}
TEST(PublicUserApiTest, DeleteUserPublic) {
    std::string username = "publicuser42";
    create_user_public(username, "pw", "nick");
    auto response = delete_user_public(username);
    EXPECT_EQ(response.status_code, 200);
    EXPECT_EQ(response.json_numbers["code"], 200);
}