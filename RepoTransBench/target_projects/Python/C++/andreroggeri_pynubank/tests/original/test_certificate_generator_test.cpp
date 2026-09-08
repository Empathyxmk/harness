#include <gtest/gtest.h>
#include "pynubank/certificate_generator.h"

TEST(CertificateGeneratorTest, BasicGeneration) {
    CertificateGenerator gen;
    auto [cert, key] = gen.generate("user");
    EXPECT_FALSE(cert.empty());
    EXPECT_FALSE(key.empty());
    // Add more certificate validation logic here
}

TEST(CertificateGeneratorTest, ThrowsOnInvalidUser) {
    CertificateGenerator gen;
    EXPECT_THROW(gen.generate(""), std::invalid_argument);
}