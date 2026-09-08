#include <gtest/gtest.h>
#include <stdexcept>
#include <string>

namespace routeros_api {
namespace base_api {
std::pair<uint64_t,int> _encode_length(uint64_t x) {
    if (x < 0x80) return {x, 1};
    if (x < 0x4000) return {(0x8000|x), 2};
    if (x < 0x200000) return {(0xC00000|x),3};
    if (x < 0x10000000) return {(0xE0000000|x),4};
    if (x < 0x200000000ull) return {(0xF000000000ull|x),5};
    throw std::logic_error("too big");
}
}
}

TEST(TestEncodeLengthPublic, test_two) {
    auto result = routeros_api::base_api::_encode_length(2);
    EXPECT_EQ(result, std::make_pair(2ULL,1));
}
TEST(TestEncodeLengthPublic, test_too_big_fails) {
    EXPECT_THROW(routeros_api::base_api::_encode_length(0x1FFFFFFFFULL), std::logic_error);
}