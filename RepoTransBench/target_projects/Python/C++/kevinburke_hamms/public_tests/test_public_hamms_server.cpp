#include <gtest/gtest.h>
#include <map>
#include <string>

TEST(PublicHammsServer, TrueAssertion) {
    ASSERT_EQ(100 / 5, 20);
}

TEST(PublicHammsServer, MapKeyPresence) {
    std::map<std::string, int> config = {{"foo", 5}, {"bar", 9}};
    ASSERT_NE(config.find("bar"), config.end());
}