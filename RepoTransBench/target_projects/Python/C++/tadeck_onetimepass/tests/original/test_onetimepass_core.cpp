#include <gtest/gtest.h>
#include "onetimepass/onetimepass.h"
#include <vector>
#include <string>
#include <stdexcept>

using namespace onetimepass;

TEST(OnetimepassCore, IsPossibleTokenAcceptsValidAndInvalid) {
    EXPECT_TRUE(is_possible_token(123456));
    EXPECT_TRUE(is_possible_token(std::string("123456")));
    std::vector<uint8_t> v1{'1','2','3','4','5','6'};
    EXPECT_TRUE(is_possible_token(std::string(reinterpret_cast<char*>(v1.data()), v1.size())));
    std::vector<uint8_t> v2{'a','b','c','d','e','f'};
    EXPECT_FALSE(is_possible_token(std::string(reinterpret_cast<char*>(v2.data()), v2.size())));
    std::vector<uint8_t> v3{'1','2','3','4','5','6','7','8'};
    EXPECT_FALSE(is_possible_token(std::string(reinterpret_cast<char*>(v3.data()), v3.size())));
    EXPECT_FALSE(is_possible_token(""));
}

TEST(OnetimepassCore, GetHOTPTokenLengthAndInvalidSecret) {
    std::vector<uint8_t> secret_vec{'M','F','R','G','G','Z','D','F','M','Z','T','W','Q','2','L','K'};
    std::string secret(secret_vec.begin(), secret_vec.end());
    int result = get_hotp(secret, 10, 8, true);
    auto result_str = std::to_string(result);
    EXPECT_TRUE(!result_str.empty());
    EXPECT_LE(result_str.length(), 8);
    // Simulate binascii.Error (e.g., throw std::invalid_argument)
    try {
        std::vector<uint8_t> bad_secret{'i','n','v','a','l','i','d','!','!','!','!','!'};
        std::string bad_secret_str(bad_secret.begin(), bad_secret.end());
        get_hotp(bad_secret_str, 1);
        FAIL() << "Expected std::invalid_argument";
    } catch (const std::invalid_argument &err) {
        SUCCEED();
    } catch (...) {
        FAIL() << "Expected std::invalid_argument";
    }
}

TEST(OnetimepassCore, GetHOTPCasefoldFalse) {
    std::vector<uint8_t> secret_vec{'m','f','r','g','g','z','d','f','m','z','t','w','q','2','l','k'};
    std::string secret(secret_vec.begin(), secret_vec.end());
    EXPECT_NO_THROW(get_hotp(secret, 1, 6, false, true));
    try {
        get_hotp(secret, 1, 6, false, false);
        FAIL() << "Expected std::invalid_argument";
    } catch (const std::invalid_argument&) {
        SUCCEED();
    } catch (...) {
        FAIL() << "Expected std::invalid_argument";
    }
}

TEST(OnetimepassCore, TOTPDefault) {
    std::vector<uint8_t> secret_vec{'M','F','R','G','G','Z','D','F','M','Z','T','W','Q','2','L','K'};
    std::string secret(secret_vec.begin(), secret_vec.end());
    int token = get_totp(secret);
    EXPECT_TRUE(typeid(token) == typeid(int));
    // "monkeypatch" for deterministic time: since not available in pure C++, this block is conceptual
    // For now, call get_totp with explicit time param
    std::size_t fake_time = 1650000000;
    int token_1 = get_totp(secret, 6, false, 30, fake_time);
    EXPECT_TRUE(typeid(token_1) == typeid(int));
}

TEST(OnetimepassCore, ValidHOTPAndLast) {
    std::vector<uint8_t> secret_vec{'M','F','R','G','G','Z','D','F','M','Z','T','W','Q','2','L','K'};
    std::string secret(secret_vec.begin(), secret_vec.end());
    int token = get_hotp(secret, 2);
    EXPECT_EQ(valid_hotp(token, secret), true); // in C++ we'll only know if valid or not
    EXPECT_EQ(valid_hotp(token, secret, 2), false);
    EXPECT_FALSE(valid_hotp(0, secret)); // "abcdef" interpreted as invalid int, 0
    try {
        std::vector<uint8_t> bad_secret{'i','n','v','a','l','i','d','s','e','c','r','e','t','!','!','!','!','!','!'};
        std::string bad_secret_str(bad_secret.begin(), bad_secret.end());
        valid_hotp(token, bad_secret_str);
        FAIL() << "Expected std::invalid_argument";
    } catch (const std::invalid_argument&) {
        SUCCEED();
    } catch (...) {
        FAIL() << "Expected std::invalid_argument";
    }
}

TEST(OnetimepassCore, GetTOTPTokenLengthAndString) {
    std::vector<uint8_t> secret_vec{'M','F','R','G','G','Z','D','F','M','Z','T','W','Q','2','L','K'};
    std::string secret(secret_vec.begin(), secret_vec.end());
    std::size_t fake_time = 1650000000;
    int result = get_totp(secret, 8, true, 30, fake_time);
    auto result_str = std::to_string(result);
    EXPECT_TRUE(!result_str.empty());
    EXPECT_LE(result_str.length(), 8);
}

TEST(OnetimepassCore, ValidTOTPAndWindow) {
    std::vector<uint8_t> secret_vec{'M','F','R','G','G','Z','D','F','M','Z','T','W','Q','2','L','K'};
    std::string secret(secret_vec.begin(), secret_vec.end());
    std::size_t fake_time = 1650000000;
    int token = get_totp(secret, 6, false, 30, fake_time);
    EXPECT_TRUE(valid_totp(token, secret, 0, 30, fake_time));
    EXPECT_TRUE(valid_totp(token, secret, 1, 30, fake_time));
    EXPECT_FALSE(valid_totp(token+1, secret, 0, 30, fake_time));
    EXPECT_FALSE(valid_totp(0, secret, 0, 30, fake_time));
    try {
        std::vector<uint8_t> bad_secret{'i','n','v','a','l','i','d','s','e','c','r','e','t','!','!','!'};
        std::string bad_secret_str(bad_secret.begin(), bad_secret.end());
        valid_totp(token, bad_secret_str, 0, 30, fake_time);
        FAIL() << "Expected std::invalid_argument";
    } catch (const std::invalid_argument&) {
        SUCCEED();
    } catch (...) {
        FAIL() << "Expected std::invalid_argument";
    }
}

TEST(OnetimepassCore, GetTOTPFIxedTime) {
    std::vector<uint8_t> secret_vec{'M','F','R','G','G','Z','D','F','M','Z','T','W','Q','2','L','K'};
    std::string secret(secret_vec.begin(), secret_vec.end());
    std::size_t fake_time = 1000;
    int token = get_totp(secret, 6, false, 30, fake_time);
    EXPECT_TRUE(typeid(token) == typeid(int));
}