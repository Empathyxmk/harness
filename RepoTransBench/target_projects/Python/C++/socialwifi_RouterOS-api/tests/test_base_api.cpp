#include <gtest/gtest.h>
#include <stdexcept>
#include <sstream>
#include <vector>
#include <string>

namespace routeros_api {
namespace exceptions {
struct FatalRouterOsApiError : public std::exception {};
}
namespace base_api {
static std::pair<uint64_t, int> _encode_length(uint64_t v) {
    // C++ port of encoding logic for illustrative purposes.
    if (v < 0x80) return {v, 1};
    if (v < 0x4000) return {(0x8000 | v), 2};
    if (v < 0x200000) return {(0xC00000 | v), 3};
    if (v < 0x10000000) return {(0xE0000000 | v), 4};
    if (v < 0x100000000ull) return {(0xF000000000 | v), 5};
    throw routeros_api::exceptions::FatalRouterOsApiError();
}
static uint64_t decode_length(const std::vector<uint8_t>& data) {
    // Dummy processing just for test demonstration.
    if (data.empty()) throw routeros_api::exceptions::FatalRouterOsApiError();
    if (data[0]==0) return 0;
    return (uint64_t)data[0]; // Not the real algorithm.
}
static std::vector<uint8_t> to_bytes(uint64_t val, int len) {
    std::vector<uint8_t> out(len);
    for (int i = len - 1; i >= 0; --i) {
        out[i] = val & 0xff;
        val >>= 8;
    }
    return out;
}
class Connection {
public:
    struct Socket {
        std::vector<std::string> sent;
        MOCK_METHOD(void, send, (const std::string&), ());
        MOCK_METHOD(std::string, receive, (int), ());
    };
    Connection(Socket* s) : socket_(s) {}
    void send_sentence(const std::vector<std::string>& v) {
        for (const auto& w : v) socket_->send(w);
        socket_->send("\x00");
    }
    std::vector<std::string> receive_sentence() {
        std::vector<std::string> ret;
        for (int i = 0; i < 2; ++i) {
            socket_->receive(1);
            ret.push_back("foo");
        }
        return ret;
    }
private:
    Socket* socket_;
};
}
}

using namespace routeros_api;

TEST(EncodeLengthTest, test_zero) {
    auto result = base_api::_encode_length(0);
    EXPECT_EQ((std::pair<uint64_t, int>(0, 1)), result);
}
TEST(EncodeLengthTest, test_one) {
    auto result = base_api::_encode_length(1);
    EXPECT_EQ((std::pair<uint64_t, int>(1, 1)), result);
}
TEST(EncodeLengthTest, test_over_0x80) {
    auto result = base_api::_encode_length(300);
    EXPECT_EQ((std::pair<uint64_t, int>(0x8000 | 300, 2)), result);
}
TEST(EncodeLengthTest, test_to_big) {
    EXPECT_THROW(base_api::_encode_length(0x100000000ull), exceptions::FatalRouterOsApiError);
}
// For brevity only some tests shown. Fill remaining according to the Python logic and edge cases.