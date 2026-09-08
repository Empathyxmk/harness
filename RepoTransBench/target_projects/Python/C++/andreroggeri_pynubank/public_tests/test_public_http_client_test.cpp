#include <gtest/gtest.h>
#include "pynubank/http_client.h"

TEST(PublicHttpClientTest, GetReturns200) {
    HttpClient client;
    auto resp = client.get("http://httpbin.org/get");
    EXPECT_EQ(resp.status, 200);
}