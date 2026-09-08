#include <gtest/gtest.h>
#include "medium.h"
#include <string>
#include <vector>
#include <map>

class TestClient : public ::testing::Test {
protected:
    virtual void SetUp() {
        client = new Client("myaccesstoken");
    }
    virtual void TearDown() {
        delete client;
    }
    Client* client;
};

// exchange_authorization_code
TEST_F(TestClient, ExchangeAuthorizationCode) {
    Client cl("myclientid", "myclientsecret");

    std::map<std::string, std::string> resp = cl.exchange_authorization_code("mycode", "http://example.com/cb");

    EXPECT_EQ(resp["access_token"], "myaccesstoken");
    EXPECT_EQ(resp["refresh_token"], "myrefreshtoken");
    EXPECT_EQ(resp["scope"], "basicProfile");
}

// exchange_refresh_token
TEST_F(TestClient, ExchangeRefreshToken) {
    Client cl("myclientid", "myclientsecret");

    std::map<std::string, std::string> resp = cl.exchange_refresh_token("myrefreshtoken");

    EXPECT_EQ(resp["access_token"], "myaccesstoken2");
    EXPECT_EQ(resp["refresh_token"], "myrefreshtoken2");
    EXPECT_EQ(resp["scope"], "basicProfile");
}

// get_current_user
TEST_F(TestClient, GetCurrentUser) {
    std::map<std::string, std::string> expected = {
        {"username", "nicki"},
        {"url", "https://medium.com/@nicki"},
        {"imageUrl", "https://images.medium.com/0*fkfQiTzT7TlUGGyI.png"},
        {"id", "5303d74c64f66366f00cb9b2a94f3251bf5"},
        {"name", "Nicki Minaj"}
    };

    auto resp = client->get_current_user();
    EXPECT_EQ(resp, expected);
}

// create_post
TEST_F(TestClient, CreatePost) {
    std::vector<std::string> tags = {"stars", "ships", "pop"};
    auto resp = client->create_post(
        "5303d74c64f66366f00cb9b2a94f3251bf5",
        "Starships",
        "<p>Are meant to flyyyy</p>",
        "html",
        tags,
        "draft"
    );

    std::map<std::string, std::string> expected = {
        {"license", "all-rights-reserved"},
        {"title", "Starships"},
        {"url", "https://medium.com/@nicki/55050649c95"},
        {"tags", "stars,ships,pop"},
        {"authorId", "5303d74c64f66366f00cb9b2a94f3251bf5"},
        {"publishStatus", "draft"},
        {"id", "55050649c95"}
    };
    EXPECT_EQ(resp, expected);
}

// upload_image
TEST_F(TestClient, UploadImage) {
    auto resp = client->upload_image("./tests/test.png", "image/png");
    std::map<std::string, std::string> expected = {
        {"url", "https://cdn-images-1.medium.com/0*dlkfjalksdjfl.jpg"},
        {"md5", "d87e1628ca597d386e8b3e25de3a18bc"}
    };
    EXPECT_EQ(resp, expected);
}