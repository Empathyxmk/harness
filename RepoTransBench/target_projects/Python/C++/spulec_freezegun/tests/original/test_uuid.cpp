#include <gtest/gtest.h>
#include <string>
#include <random>
#include <cstdint>

std::string make_uuid() {
    static uint64_t counter = 0;
    ++counter;
    return std::to_string(counter);
}

TEST(UuidTest, UUID1NotEqual) {
    auto u1 = make_uuid();
    auto u2 = make_uuid();
    ASSERT_NE(u1, u2);
}