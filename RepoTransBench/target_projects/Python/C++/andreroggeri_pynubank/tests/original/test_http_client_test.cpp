#include <gtest/gtest.h>
#include "pynubank/http_client.h"

TEST(HttpClientTest, GetRequestReturnsOk) {
    HttpClient client;
    auto response = client.get("http://httpbin.org/get");
    EXPECT_EQ(response.status, 200);
}

TEST(HttpClientTest, PostRequestReturnsOk) {
    HttpClient client;
    std::string body = "{\"foo\": \"bar\"}";
    auto response = client.post("http://httpbin.org/post", body);
    EXPECT_EQ(response.status, 200);
    EXPECT_NE(response.body.find("foo"), std::string::npos);
}