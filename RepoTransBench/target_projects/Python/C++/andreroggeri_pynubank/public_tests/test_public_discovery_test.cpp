#include <gtest/gtest.h>
#include "pynubank/discovery.h"

TEST(PublicDiscoveryTest, EndpointsContainEvents) {
    Discovery discovery;
    auto eps = discovery.getEndpoints("api");
    EXPECT_NE(eps.find("events_url"), eps.end());
}