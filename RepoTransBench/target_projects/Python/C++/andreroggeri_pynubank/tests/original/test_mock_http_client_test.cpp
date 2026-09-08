#include <gtest/gtest.h>
#include "pynubank/mock_http_client.h"

TEST(MockHttpClientTest, ReturnsMockedResponse) {
    MockHttpClient client;
    auto response = client.get("/mocked/url");
    EXPECT_EQ(response.status, 200);
    EXPECT_EQ(response.body, "{\"mocked\":true}");
}