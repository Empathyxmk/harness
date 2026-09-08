#include <gtest/gtest.h>
#include "pynubank/certificate_generator.h"

TEST(PublicCertificateGeneratorTest, GeneratesNonempty) {
    CertificateGenerator gen;
    auto [cert, key] = gen.generate("publicuser");
    EXPECT_FALSE(cert.empty());
    EXPECT_FALSE(key.empty());
}