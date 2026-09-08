#include <gtest/gtest.h>
#include "pynubank/mock_http_client.h"

TEST(PublicMockHttpClientTest, HasMockedData) {
    MockHttpClient client;
    auto resp = client.get("/mocked/url");
    EXPECT_EQ(resp.status, 200);
}