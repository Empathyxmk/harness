#include <gtest/gtest.h>
#include "src/lib/txweb.h"

TEST(PublicTxwebTest, ErrorProperties) {
    Error err(1000, "unknown error", {{"prop", "value"}});
    EXPECT_EQ(err.code, 1000);
    EXPECT_EQ(err.message, "unknown error");
    EXPECT_EQ(err.data.at("prop"), "value");
}

TEST(PublicTxwebTest, ErrorStrRepr) {
    Error err(404, "resource not here");
    EXPECT_EQ(err.str(), "resource not here");
    EXPECT_EQ(err.repr(), "Error(404, 'resource not here')");
}

TEST(PublicTxwebTest, HandlerReturnsNotFound) {
    class DummyHandler : public Handler {
    public:
        void operator()() override { throw NOT_FOUND; }
    };

    DummyHandler handler;
    try {
        handler();
        FAIL();
    } catch(const Error& e) {
        EXPECT_EQ(e.code, 404);
        EXPECT_EQ(e.message, "Not Found");
    }
}