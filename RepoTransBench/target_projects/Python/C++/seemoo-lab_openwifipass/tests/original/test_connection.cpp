#include <gtest/gtest.h>
#include "lib/Connection.h"

// Dummy handler for method call verification
class DummyPWSHandler {
public:
    std::vector<std::pair<std::string, std::vector<uint8_t>>> calls;
    void receivePWS2(const std::vector<uint8_t>& x) { calls.emplace_back("pws2", x); }
    void receiveM2(const std::vector<uint8_t>& x) { calls.emplace_back("m2", x); }
    void receiveM4(const std::vector<uint8_t>& x) { calls.emplace_back("m4", x); }
    void receivePWS4(const std::vector<uint8_t>& x) { calls.emplace_back("pws4", x); }
};

TEST(ConnectionSuite, HandleNotificationMainPaths) {
    struct Param { int ft, state; std::string exp; } params[] = {
        {24, 0, "pws2"}, {19, 1, "m2"}, {19, 2, "m4"}, {6,  3, "pws4"}
    };
    for (const auto& p : params) {
        DummyPWSHandler handler;
        // WPNearbyReadDelegate should accept handler and expose members like state, openFrame, payload etc.
        WPNearbyReadDelegate d(&handler); // simulate the stub in C++
        d.state = p.state;
        d.openFrame = true;
        std::vector<uint8_t> pl = {static_cast<uint8_t>(p.ft), 42};
        pl.insert(pl.end(), {'r','e','s','t'}); // 'rest'
        d.payload = pl;
        d.expectedPayloadLength = pl.size();
        d.handleNotification(nullptr, std::vector<uint8_t>());
        ASSERT_FALSE(handler.calls.empty());
        EXPECT_EQ(handler.calls[0].first, p.exp);
    }
}

// Other tests from test_connection.py would continue in similar style with C++ stubbing, GoogleTest mocks and logic mapping.