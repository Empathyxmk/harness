#include <gtest/gtest.h>
#include "pynubank/discovery.h"

TEST(DiscoveryTest, GetsEndpoints) {
    Discovery discovery;
    auto endpoints = discovery.getEndpoints("api");
    EXPECT_FALSE(endpoints.empty());
    EXPECT_NE(endpoints.find("events_url"), endpoints.end());
}