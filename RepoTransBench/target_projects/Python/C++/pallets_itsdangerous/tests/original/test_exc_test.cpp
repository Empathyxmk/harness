#include <gtest/gtest.h>
#include "itsdangerous_exceptions.h"

#include <chrono>
#include <ctime>
#include <stdexcept>
#include <string>

TEST(ExceptionTest, BadDataStrAndMessage) {
    BadData err("msg-1");
    EXPECT_STREQ(err.what(), "msg-1");
    EXPECT_EQ(err.message(), "msg-1");
}

TEST(ExceptionTest, BadSignaturePayload) {
    BadSignature err("fail sig", "abc");
    EXPECT_STREQ(err.what(), "fail sig");
    EXPECT_EQ(err.payload(), "abc");
}

TEST(ExceptionTest, BadTimeSignaturePayloadAndDate) {
    std::time_t now = std::time(nullptr);
    BadTimeSignature err("fail time sig", "bbb", now);
    EXPECT_EQ(err.message(), "fail time sig");
    EXPECT_EQ(err.payload(), "bbb");
    EXPECT_EQ(err.date_signed(), now);
}

TEST(ExceptionTest, SignatureExpiredIsSubclass) {
    // In C++: use RTTI/dynamic_cast for inheritance
    SignatureExpired ex("expired!");
    BadTimeSignature* bts_ptr = dynamic_cast<BadTimeSignature*>(&ex);
    EXPECT_TRUE(bts_ptr != nullptr);
}

TEST(ExceptionTest, BadHeaderPayloadAndError) {
    std::runtime_error orig_ex("boom");
    BadHeader bh("bad head", "yy", {{"x","y"}}, &orig_ex);
    EXPECT_EQ(bh.message(), "bad head");
    EXPECT_EQ(bh.payload(), "yy");
    EXPECT_EQ(bh.header().at("x"), "y");
    EXPECT_EQ(bh.original_error(), &orig_ex);
}

TEST(ExceptionTest, BadPayloadOriginalError) {
    std::invalid_argument orig("failz");
    BadPayload bp("bad pay", &orig);
    EXPECT_EQ(bp.message(), "bad pay");
    EXPECT_EQ(bp.original_error(), &orig);
}