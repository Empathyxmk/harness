#include <gtest/gtest.h>
#include "itsdangerous_exceptions.h"

TEST(ExceptionPublicTest, BadSignatureStrPublic) {
    BadSignature sig("Diff reason");
    EXPECT_NE(std::string(sig.what()).find("Diff reason"), std::string::npos);
}
TEST(ExceptionPublicTest, BadPayloadStrPublic) {
    BadPayload bp("Different");
    EXPECT_NE(std::string(bp.what()).find("Different"), std::string::npos);
}
TEST(ExceptionPublicTest, BadTimeSignatureStrPublic) {
    BadTimeSignature bts("ReasonZZZ");
    EXPECT_NE(std::string(bts.what()).find("ReasonZZZ"), std::string::npos);
}
TEST(ExceptionPublicTest, SignatureExpiredStrPublic) {
    SignatureExpired se("Late!");
    EXPECT_NE(std::string(se.what()).find("Late!"), std::string::npos);
}