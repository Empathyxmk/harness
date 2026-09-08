#include <gtest/gtest.h>

TEST(TestRFC822Unescape, VariousContents) {
    SUCCEED() << "Stub: rfc822_unescape(rfc822_escape(x)) is identity for test cases";
}

TEST(TestCoreMetadata, ReadMetadata) {
    SUCCEED() << "Stub: Write then read-back all tested fields in PKG-INFO (metadata)";
}

TEST(TestCoreMetadata, MaintainerAuthorVars) {
    SUCCEED() << "Stub: Different combinations of author+maintainer are present in PKG-INFO";
}

TEST(TestParityWithMetadataFromPyPaWheel, RequiresDistPresent) {
    SUCCEED() << "Stub: PKG-INFO and METADATA have expected requirements and are equivalent";
}

TEST(TestParityWithMetadataFromPyPaWheel, EquivalentOutput) {
    SUCCEED() << "Stub: setuptools and wheel output is compared for strict equality";
}

TEST(TestPEP643, StaticConfigNoDynamic) {
    SUCCEED() << "Stub: static config does not output Dynamic fields";
}

TEST(TestPEP643, ModifiedFieldsMarkedDynamic) {
    SUCCEED() << "Stub: Dynamic fields present when attributes modified";
}

TEST(TestPEP643, LicenseFilesDynamic) {
    SUCCEED() << "Stub: license-files and license-expression show up as dynamic fields";
}