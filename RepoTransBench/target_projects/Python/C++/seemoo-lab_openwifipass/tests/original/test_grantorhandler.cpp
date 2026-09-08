#include <gtest/gtest.h>
#include "lib/GrantorHandler.h"

// We assume the GrantorHandler C++ module exposes PWSGrantorHandler class

TEST(GrantorHandler, HandlerCreation) {
    PWSGrantorHandler handler;
    EXPECT_TRUE(typeid(handler) == typeid(PWSGrantorHandler));
}

TEST(GrantorHandler, ParseRequestWrongType) {
    PWSGrantorHandler handler;
    std::map<std::string, std::string> payload = {{"type", "1000"}, {"payload", "random"}};
    auto result = handler.parseRequest(payload);
    EXPECT_TRUE(result == nullptr || result == nullptr);
}

TEST(GrantorHandler, GetSSID) {
    PWSGrantorHandler handler;
    EXPECT_EQ(handler.getSSID(), "");
}

TEST(GrantorHandler, GetPassword) {
    PWSGrantorHandler handler;
    EXPECT_EQ(handler.getPassword(), "");
}

TEST(GrantorHandler, Authorize) {
    PWSGrantorHandler handler;
    EXPECT_EQ(handler.authorize(), true);
}

TEST(GrantorHandler, MethodsDefaultWithSession) {
    PWSGrantorHandler handler;
    // Simulate monkeypatching session member
    struct DummySession {
        std::string ssid = "myssid";
        std::string password = "pw";
    };
    handler.session = std::make_shared<DummySession>();
    EXPECT_EQ(handler.getSSID(), "myssid");
    EXPECT_EQ(handler.getPassword(), "pw");
}