#include <gtest/gtest.h>
#include <string>

class AccessToken {
public:
    std::string token;
    AccessToken(const std::string& tk) : token(tk) {}
};

TEST(TestPostAuth, Sync) {
    AccessToken response("SOMETOKEN");
    ASSERT_EQ(response.token, "SOMETOKEN");
}

TEST(TestPostAuth, SyncHeaders) {
    AccessToken response("SOMETOKEN");
    ASSERT_EQ(response.token, "SOMETOKEN");
}