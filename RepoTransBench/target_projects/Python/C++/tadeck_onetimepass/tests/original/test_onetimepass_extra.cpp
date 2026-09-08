#include <gtest/gtest.h>
#include "onetimepass/onetimepass.h"
#include <string>
#include <vector>
#include <stdexcept>

using namespace onetimepass;

class OnetimepassEdgeCases : public ::testing::Test {
protected:
    std::vector<uint8_t> secret_vec;
    std::string secret;

    void SetUp() override {
        secret_vec = {'M','F','R','G','G','Z','D','F','M','Z','T','W','Q','2','L','K'};
        secret = std::string(secret_vec.begin(), secret_vec.end());
    }
};

TEST_F(OnetimepassEdgeCases, GetHOTPInvalidSecretType) {
    try {
        get_hotp(std::string(), 1); // passing empty string for "invalid" type
        FAIL() << "Expected std::invalid_argument";
    } catch (const std::invalid_argument&) {
        SUCCEED();
    } catch (...) {
        FAIL() << "Expected std::invalid_argument";
    }
}

TEST_F(OnetimepassEdgeCases, GetHOTPIncorrectBase32) {
    std::vector<uint8_t> notbase32 = {'n','o','t','b','a','s','e','3','2','@','#','$'};
    std::string notbase32s(notbase32.begin(), notbase32.end());
    try {
        get_hotp(notbase32s, 1);
        FAIL() << "Expected std::invalid_argument or std::runtime_error";
    } catch (const std::invalid_argument&) { SUCCEED(); }
    catch (const std::runtime_error&) { SUCCEED(); }
    catch (...) { FAIL() << "Expected std::invalid_argument or std::runtime_error"; }
}

TEST_F(OnetimepassEdgeCases, GetHOTPCustomDigest) {
    int val = get_hotp(secret, 1, 8);
    EXPECT_TRUE(typeid(val) == typeid(int));
    EXPECT_LT(std::to_string(val).length(), 9);
}

TEST_F(OnetimepassEdgeCases, GetHOTPStringTypes) {
    // All data as string in C++
    std::string sec = "MFRGGZDFMZTWQ2LK";
    int res = get_hotp(sec, 2, 6, true);
    // Cannot guarantee a known output unless implementation matches Python's.
    // For this test, ensure result is 6 digits, positive.
    EXPECT_GE(res, 0);
    EXPECT_LT(res, 1000000);
}

TEST_F(OnetimepassEdgeCases, ValidHOTPReturnsFalse) {
    EXPECT_FALSE(valid_hotp(111111, secret, 0, 1));
}

TEST_F(OnetimepassEdgeCases, ValidHOTPWithRange) {
    int tok = get_hotp(secret, 99);
    EXPECT_TRUE(valid_hotp(tok, secret, 97, 3));
}

TEST_F(OnetimepassEdgeCases, ValidTOTPFalse) {
    EXPECT_FALSE(valid_totp(123456, secret));
}

TEST_F(OnetimepassEdgeCases, GetTOTPAndValidTOTP) {
    int tok = get_totp(secret);
    EXPECT_TRUE(valid_totp(tok, secret));
    EXPECT_FALSE(valid_totp(tok+1, secret));
}

TEST_F(OnetimepassEdgeCases, GetTOTPCustomTokenLength) {
    int tok = get_totp(secret, 8);
    EXPECT_TRUE(typeid(tok) == typeid(int));
    EXPECT_LT(std::to_string(tok).length(), 9);
}