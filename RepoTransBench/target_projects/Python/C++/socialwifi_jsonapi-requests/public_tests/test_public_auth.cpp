#include <gtest/gtest.h>
#include <string>

// Mocks to simulate original Python classes/fields
namespace auth {
    struct BasicAuth {
        BasicAuth(const std::string& u, const std::string& p): username(u), password(p) {}
        std::string username, password;
    };
    struct TokenAuth {
        TokenAuth(const std::string& t): token(t) {}
        std::string token;
    };
}
struct DummyConfig {
    void set_auth(const auth::BasicAuth& a) { AUTH = a; }
    auth::BasicAuth AUTH = auth::BasicAuth("", "");
};

TEST(PublicAuthTest, test_basic_auth_public) {
    auth::BasicAuth a("user2", "pass2");
    EXPECT_EQ(a.username, "user2");
    EXPECT_EQ(a.password, "pass2");
}

TEST(PublicAuthTest, test_token_auth_public) {
    auth::TokenAuth t("publictoken");
    EXPECT_EQ(t.token, "publictoken");
}

TEST(PublicAuthTest, test_apply_auth_public) {
    auth::BasicAuth a("alice", "secret123");
    DummyConfig config;
    config.set_auth(a);
    EXPECT_EQ(config.AUTH.username, "alice");
    EXPECT_EQ(config.AUTH.password, "secret123");
}