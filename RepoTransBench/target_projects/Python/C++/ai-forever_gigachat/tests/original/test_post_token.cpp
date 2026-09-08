#include <gtest/gtest.h>
#include <string>

class Token {
public:
    std::string token;
    Token(const std::string& t) : token(t) {}
};

TEST(TestPostToken, Sync) {
    Token response("TOKENVAL");
    ASSERT_EQ(response.token, "TOKENVAL");
}

TEST(TestPostToken, SyncHeaders) {
    Token response("TOKENVAL");
    ASSERT_EQ(response.token, "TOKENVAL");
}