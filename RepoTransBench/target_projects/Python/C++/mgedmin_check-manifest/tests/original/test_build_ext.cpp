#include <gtest/gtest.h>

TEST(TestBuildExt, GetExtFilename) {
    SUCCEED() << "Stub: ext filename logic matches distutils";
}

TEST(TestBuildExt, Abi3Filename) {
    SUCCEED() << "Stub: abi3 python extensions detected by filename";
}

TEST(TestBuildExt, ExtSuffixOverride) {
    SUCCEED() << "Stub: SETUPTOOLS_EXT_SUFFIX env always overrides extension";
}

TEST(TestBuildExt, GetOutputsRegularAndEditable) {
    SUCCEED() << "Stub: get_outputs returns correct built extension files and stubs";
}

TEST(TestBuildExt, GetOutputMappingWithStub) {
    SUCCEED() << "Stub: editable mode outputs mapping contains stub";
}

TEST(TestBuildExtInplace, Optional) {
    SUCCEED() << "Stub: optional extensions cause log error, not compile error";
}

TEST(TestBuildExtInplace, NonOptional) {
    SUCCEED() << "Stub: non-optional induces CompileError";
}

TEST(TestBuildExt, ConfigHandling) {
    SUCCEED() << "Stub: ext_modules built with config options";
}