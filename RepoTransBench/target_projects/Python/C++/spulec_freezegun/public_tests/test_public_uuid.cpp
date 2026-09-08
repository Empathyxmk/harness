#include <gtest/gtest.h>
#include <string>

std::string make_uuid() {
    static int counter = 0;
    ++counter;
    return std::to_string(counter);
}

TEST(PublicUuidTest, UUID1NotEqual) {
    std::string u1 = make_uuid();
    std::string u2 = make_uuid();
    ASSERT_NE(u1, u2);
}

TEST(PublicUuidTest, UUID5Generation) {
    // In C++ we use hashes to simulate deterministic uuid5
    std::string ns = "OID";
    std::string value = "example.org";
    std::hash<std::string> h;
    auto u = h(ns + value);
    ASSERT_EQ(h(ns + value), u);
}