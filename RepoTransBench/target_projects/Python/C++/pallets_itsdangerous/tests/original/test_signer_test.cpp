#include <gtest/gtest.h>
#include "signer.h"
#include <vector>
#include <string>

TEST(SignerTest, SignUnsign) {
    Signer signer("test-secret");
    std::vector<uint8_t> value{'a','b','c'};
    auto signedv = signer.sign(value);
    EXPECT_EQ(signer.unsign(signedv), value);
}

TEST(SignerTest, InvalidSignature) {
    Signer signer("test-secret");
    std::vector<uint8_t> bad{'i','n','v','a','l','i','d','-','d','a','t','a'};
    auto bad_input = bad;
    bad_input.insert(bad_input.end(), {'.','b','a','d'});
    EXPECT_THROW({
        signer.unsign(bad_input);
    }, BadSignature);
}

TEST(SignerTest, KeyDerivation) {
    Signer s1("secret", "a");
    Signer s2("secret", "b");
    auto sig1 = s1.sign({'d','a','t','a'});
    auto sig2 = s2.sign({'d','a','t','a'});
    EXPECT_NE(sig1, sig2);
}

TEST(SignerTest, Separates) {
    Signer s("test-secret", "--");
    std::vector<uint8_t> val{'x','y','z'};
    auto signedval = s.sign(val);
    EXPECT_EQ(s.unsign(signedval), val);
    int seps = std::count(signedval.begin(), signedval.end(), '-');
    EXPECT_EQ(seps, 2);
}

TEST(SignerTest, SignatureCheck) {
    Signer signer("secret");
    std::vector<uint8_t> value{'f','o','o'};
    auto signedv = signer.sign(value);
    EXPECT_EQ(signer.unsign(signedv), value);

    auto tampered = signedv;
    tampered.back() = tampered.back() == '0' ? '1' : '0';
    EXPECT_THROW({
        signer.unsign(tampered);
    }, BadSignature);
}