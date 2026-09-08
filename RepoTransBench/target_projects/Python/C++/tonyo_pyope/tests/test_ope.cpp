#include <gtest/gtest.h>
#include <vector>
#include <algorithm>
#include "ope.h"

// Helper: For b'...' keys. We'll use std::vector<uint8_t> or std::string as key stand-ins.
// The actual implementation would depend on your OPE class.

TEST(OPE, OrderGuarantees) {
    // "Test that encryption is order-preserving"
    std::vector<int64_t> values = {0, 1, 2, 10, 28, 42, 1000, 1001, (1 << 15) - 1};
    std::string key = "key";
    OPE cipher(key);
    std::vector<int64_t> encrypted_values;
    for (auto value : values) {
        encrypted_values.push_back(cipher.encrypt(value));
    }
    std::vector<int64_t> sorted_encrypted(encrypted_values.begin(), encrypted_values.end());
    std::sort(sorted_encrypted.begin(), sorted_encrypted.end());
    sorted_encrypted.erase(std::unique(sorted_encrypted.begin(), sorted_encrypted.end()), sorted_encrypted.end());
    EXPECT_EQ(encrypted_values, sorted_encrypted) << "Order is not preserved";
}

TEST(OPE, EncryptDecrypt) {
    // "Encrypt and then decrypt"
    std::vector<int64_t> values = {-1000, -100, -20, -1, 0, 1, 10, 100, 314, 1337, 1338, 10000};
    std::string key = "key";
    ValueRange in_range(-1000, 1 << 20);
    ValueRange out_range(-10000, (int64_t)1 << 32);
    OPE cipher(key, in_range, out_range);
    std::vector<int64_t> encrypted_values;
    for (auto value : values) {
        encrypted_values.push_back(cipher.encrypt(value));
    }
    OPE cipher_dec(key, in_range, out_range);
    for (size_t i = 0; i < values.size(); ++i) {
        int64_t decrypted = cipher_dec.decrypt(encrypted_values[i]);
        EXPECT_EQ(values[i], decrypted) << "Dec(Enc(P)) != P";
    }
}

TEST(OPE, Deterministic) {
    // "Test that encrypting the same values yields the same results"
    std::vector<int64_t> values = {0, 314, 1337, 1338, 10000};
    std::string key = "key-la-la";
    OPE cipher(key);
    std::vector<int64_t> encrypted_first;
    std::vector<int64_t> encrypted_second;
    for (auto v : values) encrypted_first.push_back(cipher.encrypt(v));
    for (auto v : values) encrypted_second.push_back(cipher.encrypt(v));
    EXPECT_EQ(encrypted_first, encrypted_second);
}

TEST(OPE, DenseRange) {
    // "Equal ranges must yield 1-to-1 mapping"
    int64_t range_start = 0;
    int64_t range_end = 1 << 15;
    ValueRange in_range(range_start, range_end);
    ValueRange out_range = in_range.copy();
    std::string key = "123";
    OPE cipher(key, in_range, out_range);
    std::vector<int64_t> values = {0, 10, 20, 50, 100, 1000, 1 << 10, 1 << 15};
    for (auto v : values) {
        EXPECT_EQ(cipher.encrypt(v), v);
        EXPECT_EQ(cipher.decrypt(v), v);
    }
    EXPECT_THROW({
        OPE(key, ValueRange(0, 10), ValueRange(1, 2));
    }, std::exception);
}

TEST(OPE, LongDifferentKeys) {
    // "Test that different keys yield different ciphertexts"
    std::string key1("\x12\x23\x34\x45\x56\x67\x78\x89\x90\x0A\xAB\xBC\xCD\xDE\xEF\xF0\x13\x14\x15\x16", 20);
    std::string key2("\x0A\xAB\xBC\xCD\xDE\xEF\xF0\x13\x14\x15\x16\x12\x23\x34\x45\x56\x67\x78\x89\x90\x12\x13", 22);
    OPE ope1(key1), ope2(key2);
    std::vector<int64_t> values = {0, 1, 10, 100, 1000, 2000, 3000, 4000, 5000};
    for (auto v : values) {
        EXPECT_NE(ope1.encrypt(v), ope2.encrypt(v));
    }
}

TEST(OPE, EncryptSmallOutRangeIssue) {
    // "Regression test for this issue: https://github.com/tonyo/pyope/issues/13"
    OPE cipher(
        "fresh key",
        ValueRange(0, 2),
        ValueRange(2, 5)
    );
    EXPECT_NO_THROW(cipher.encrypt(0));
    EXPECT_NO_THROW(cipher.encrypt(1));
    EXPECT_NO_THROW(cipher.encrypt(2));
}

TEST(OPE, BigRanges) {
    ValueRange in_range((int64_t)1 << 32, (int64_t)1 << 33);
    ValueRange out_range((int64_t)1 << 48, (int64_t)1 << 49);
    OPE ope("test-big-ranges", in_range, out_range);
    int64_t plaintext = in_range.start;
    while (plaintext <= in_range.end) {
        EXPECT_NO_THROW(ope.encrypt(plaintext));
        plaintext += ((int64_t)1 << 24);
    }
}

TEST(OPE, HugeOutputRange) {
    // "Regression test for https://github.com/tonyo/pyope/pull/16"
    OPE cipher("key11",
        ValueRange(0, 0),
        ValueRange(0, (int64_t)1 << 65)
    );
    EXPECT_NO_THROW(cipher.encrypt(0));
}