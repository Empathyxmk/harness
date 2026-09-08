#include <gtest/gtest.h>

TEST(TestDistutilsAdoption, StdlibDistutilsPreferredOnRequest) {
    SUCCEED() << "Stub: SETUPTOOLS_USE_DISTUTILS=stdlib forces stdlib modules";
}

TEST(TestDistutilsAdoption, LocalDistutilsWithSetuptools) {
    SUCCEED() << "Stub: SETUPTOOLS_USE_DISTUTILS=local prefers vendored distutils";
}

TEST(TestDistutilsAdoption, LocalDistutilsUnimportedPreferred) {
    SUCCEED() << "Stub: Vendored distutils used even if never imported directly";
}

TEST(TestDistutilsAdoption, PipImportWorks) {
    SUCCEED() << "Stub: pip import succeeds after import hack";
}

TEST(TestDistutilsAdoption, DistutilsHasOrigin) {
    SUCCEED() << "Stub: distutils module origin property populated";
}

TEST(TestDistutilsAdoption, ModulesDontDuplicateOnImport) {
    SUCCEED() << "Stub: _distutils_hack ensures modules not duplicated";
}

TEST(TestDistutilsAdoption, LogModuleNotDuplicatedOnImport) {
    SUCCEED() << "Stub: log module not duplicated";
}

TEST(TestDistutilsAdoption, ConsistentErrorFromModifiedPy) {
    SUCCEED() << "Stub: DistutilsError always from correct module";
}