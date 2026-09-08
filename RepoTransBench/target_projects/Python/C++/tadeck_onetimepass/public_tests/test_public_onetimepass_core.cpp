#include <gtest/gtest.h>
#include "onetimepass/onetimepass.h"
#include <string>

using namespace onetimepass;

TEST(PublicOnetimepassCore, GetTOTP) {
    std::string secret = "12345678901234567890";
    int code = get_totp(secret, 6, false, 30, 1600000000);
    EXPECT_GE(code, 100000);
    EXPECT_LT(code, 1000000);
}

TEST(PublicOnetimepassCore, ValidTOTPToken) {
    std::string secret = "22222222222222222222";
    int code = get_totp(secret, 6, false, 30, 1600001000);
    EXPECT_TRUE(valid_totp(code, secret, 0, 30, 1600001000));
}

TEST(PublicOnetimepassCore, InvalidTOTPToken) {
    std::string secret = "33333333333333333333";
    int code = get_totp(secret, 6, false, 30, 1600010000);
    int wrong_code = (code + 10) % 1000000;
    EXPECT_FALSE(valid_totp(wrong_code, secret, 0, 30, 1600010000));
}

TEST(PublicOnetimepassCore, GetHOTP) {
    std::string secret = "JBSWY3DPEHPK3PXP";
    int code = get_hotp(secret, 7);
    EXPECT_GE(code, 100000);
    EXPECT_LT(code, 1000000);
}

TEST(PublicOnetimepassCore, ValidHOTPTrue) {
    std::string secret = "JBSWY3DPEHPK3PXQ";
    int code = get_hotp(secret, 42);
    EXPECT_TRUE(valid_hotp(code, secret, 42));
}

TEST(PublicOnetimepassCore, ValidHOTPFalse) {
    std::string secret = "JBSWY3DPEHPK3PXR";
    int code = get_hotp(secret, 53);
    EXPECT_FALSE(valid_hotp(code + 1, secret, 53));
}